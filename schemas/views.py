import csv
import datetime
import io
import random
import boto3
from botocore.config import Config

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from schemas.extra_functions import generate_presigned_url, generate_data, create_save_csv, fill_data
from schemas.forms import LoginForm, SchemaForm, ColumnFormset, FileCSVForm
from schemas.models import Schema, Column, FileCSV
import uuid


class SchemaListView(LoginRequiredMixin, generic.ListView):
    model = Schema

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("user").filter(user__id=self.request.user.id)


class NewLoginView(LoginView):
    form_class = LoginForm


def logout_view(request):
    logout(request)
    return redirect("/")


class SchemaCreateView(generic.edit.CreateView):
    model = Schema
    template_name = "../templates/schemas/schema_form.html"
    form_class = SchemaForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        ColumnFormset.extra = 1
        if self.request.POST:
            data['column_formset'] = ColumnFormset(self.request.POST)
        else:
            data['column_formset'] = ColumnFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        columns = context['column_formset']
        form.instance.user = self.request.user
        if columns.is_valid() and form.is_valid():
            self.object = form.save()
            columns.instance = self.object
            columns.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('schemas:schema-list')


class SchemaUpdateView(generic.edit.UpdateView):
    model = Schema
    template_name = "../templates/schemas/schema_form.html"
    form_class = SchemaForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        ColumnFormset.extra = 0
        if self.request.POST:
            data['column_formset'] = ColumnFormset(self.request.POST, instance=self.object)
        else:
            data['column_formset'] = ColumnFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        columns = context['column_formset']
        if columns.is_valid() and form.is_valid():
            self.object = form.save()
            form.instance.modified = datetime.date.today()
            columns.instance = self.object
            columns.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('schemas:schema-list')


class SchemaDeleteView(generic.DeleteView):
    model = Schema
    success_url = reverse_lazy("schemas:schema-list")


def schema_files(request, pk):
    schema = Schema.objects.get(id=pk)
    columns = list(Column.objects.filter(schema_id=pk))
    files = list(FileCSV.objects.filter(schema_id=pk))
    form = FileCSVForm

    if request.method == "POST":
        response, context = {}, {}
        form = FileCSVForm(request.POST)
        if form.is_valid():
            form.instance.file_name = f"schema_{str(uuid.uuid4())}.csv"
            bucket_url = generate_presigned_url(form.instance.file_name)
            form.instance.file_path = bucket_url
            form.instance.schema = schema
            record = form.save()

            data = fill_data(pk, record.rows)

            create_save_csv(
                data=data,
                file_name=form.instance.file_name,
                column_separator=schema.column_separator,
                string_character=schema.string_character
            )

            context = {
                'created': record.created,
                'rows': record.rows,
                'bucket_url': bucket_url,
                'result': 'success'
            }
        else:
            context = {'response': "Invalid rows input", 'result': 'error'}
            return JsonResponse(context, status=400)
        return JsonResponse(context)

    return render(
        request,
        "schemas/file_csv.html",
        {"form": form, "schema": schema, "columns": columns, "files": files}
    )

from django.utils.translation import gettext as _
from django.core.exceptions import MultipleObjectsReturned
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from app.common.permissions import IsDev, IsHS, is_admin_user
from app.content.models import Page
from app.content.serializers import (
    PageCreateSerializer,
    PageSerializer,
    PageTreeSerializer
)


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [IsHS | IsDev]
    lookup_url_kwarg = "path"
    lookup_value_regex = "[\w\d_/-]+"

    def get_page_from_tree(self):
        return Page.get_by_path(self.kwargs["path"])

    def retrieve(self, request, *args, **kwargs):
        try:
            post = self.get_page_from_tree()
            serializer = PageSerializer(post, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Page.DoesNotExist:
            return Response(
                {"detail": _("Fant ikke siden")}, status=status.HTTP_404_NOT_FOUND
            )
        except MultipleObjectsReturned:
            return Response(
                {"detail": _("Fant ikke siden fordi treet er ødelagt")},
                status=status.HTTP_404_NOT_FOUND,
            )

    def list(self, request, *args, **kwargs):
        try:
            post = self.queryset.get(parent=None)
            serializer = PageSerializer(post, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Page.DoesNotExist:
            return Response(
                {"detail": _("Fant ikke siden")}, status=status.HTTP_404_NOT_FOUND
            )
        except MultipleObjectsReturned:
            return Response(
                {"detail": _("Fant ikke siden fordi treet er ødelagt")},
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request, *args, **kwargs):
        if "path" not in kwargs:
            return Response(
                {"detail": _("Urlen må innholde referanse til side treet")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            parent_id = self.get_page_from_tree().Page_id
            request.data["parent"] = parent_id
            serializer = PageCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                {"detail": _("En annen side med dette navnet eksisterer allerede i denne kategorien")}, status=status.HTTP_400_BAD_REQUEST
            )
        except Page.DoesNotExist:
            return Response(
                {"detail": _("Fant ikke siden")}, status=status.HTTP_404_NOT_FOUND
            )
        except MultipleObjectsReturned:
            return Response(
                {"detail": _("Fant ikke siden fordi treet er ødelagt")},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            print(e)

    def update(self, request, *args, **kwargs):
        if "path" not in kwargs:
            return Response(
                {"detail": _("Urlen må innholde referanse til side treet")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            post = self.get_page_from_tree()
            serializer = PageSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                {"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        except Page.DoesNotExist:
            return Response(
                {"detail": _("Fant ikke siden")}, status=status.HTTP_404_NOT_FOUND
            )
        except MultipleObjectsReturned:
            return Response(
                {"detail": _("Fant ikke siden fordi treet er ødelagt")},
                status=status.HTTP_404_NOT_FOUND,
            )

    def destroy(self, request, *args, **kwargs):
        if "path" not in kwargs:
            return Response(
                {"detail": _("Urlen må innholde referanse til side treet")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            post = self.get_page_from_tree()
            if is_admin_user(request):
                self.perform_destroy(post)
                return Response(
                    {"detail": _("siden ble slettet")}, status=status.HTTP_200_OK,
                )
            return Response(
                {"detail": _("Ikke riktig tilatelse for å slette en siden")},
                status=status.HTTP_403_FORBIDDEN,
            )

        except Page.DoesNotExist:
            return Response(
                {"detail": _("Fant ikke siden")}, status=status.HTTP_404_NOT_FOUND
            )
        except MultipleObjectsReturned:
            return Response(
                {"detail": _("Fant ikke siden, fordi treet er ødelagt")},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=False, methods=['get'])
    def tree(self, request, *args, **kwargs):
        root = Page.objects.get(parent = None)
        serializer = PageTreeSerializer(root)
        return Response(serializer.data, status=status.HTTP_200_OK)

from app.group.models.membership import MembershipHistory
from rest_framework import status, viewsets
from rest_framework.response import Response

from app.group.models import Membership, Group
from app.content.models import User
from app.group.serializers import MembershipSerializer
from app.common.permissions import is_admin_user


class MembershipViewSet(viewsets.ModelViewSet):
        """API endpoint for Groups"""

        serializer_class = MembershipSerializer
        queryset = Membership.objects.all()
        permission_classes = []

        def retrieve(self, request, slug, pk):
            """Returns a spesific membership by slug"""
            try:
                membership = Membership.objects.get(user__user_id=pk, group__slug=slug)
                serializer = MembershipSerializer(
                    membership, context={"request": request}, many=False
                )
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            except Membership.DoesNotExist:
                return Response(
                    {"detail": ("Medlemskapet eksisterer ikke")},
                    status=status.HTTP_404_NOT_FOUND,
                )

        def update(self, request, *args, **kwargs):
            """Updates a spesific group by slug"""
            try:
                membership = Membership.objects.get(user__user_id=kwargs["pk"], group__slug=kwargs["slug"])
                serializer = MembershipSerializer(membership, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
            except Membership.DoesNotExist:
                return Response(
                    {"detail": ("Medlemskapet eksisterer ikke")},
                    status=status.HTTP_404_NOT_FOUND,
                )
                
        def create(self, request, *args, **kwargs):
            """Creates a group if it does not exist"""
            try:
                group = Group.objects.get(slug=kwargs["slug"])
                user = User.objects.get(user_id=request.data["user"]["user_id"])
                membership = Membership.objects.get_or_create(user = user, group = group)
                serializer = MembershipSerializer(membership[0],data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                    )
            except Membership.DoesNotExist:
                return Response(
                    {"detail": ("Medlemskapet eksisterer ikke")},
                    status=status.HTTP_404_NOT_FOUND,
                )
        def destroy(self, request, slug, pk):
            membership = Membership.objects.get(user__user_id=pk, group__slug=slug)
            print(membership)
            if is_admin_user(request):
                MembershipHistory.from_membership(membership)
                self.perform_destroy(membership)
                return Response(
                    {"detail": ("Medlemskap har blitt slettet")},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"detail": ("Ikke riktig tilatelse for å slette et medlemskap")},
                status=status.HTTP_403_FORBIDDEN,
            )
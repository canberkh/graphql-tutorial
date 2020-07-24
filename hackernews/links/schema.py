import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model

from .models import Link, User


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()

    # 2
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    # 3
    def mutate(self, info, url, description):
        link = Link(url=url, description=description)
        link.save()

        return CreateLink(id=link.id, url=link.url, description=link.description,)


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(username=username, email=email,)
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)
    users = graphene.List(UserType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()

    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.all()

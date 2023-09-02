from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters
from rest_framework.response import Response

from src.store.models import Product, Category, ProductCategory
from src.store.serializers import CategorySerializer, ProductCreateSerializer, ProductUpdateSerializer, \
    ProductDeleteSerializer, ProductListSerializer


# Create your views here.

class CategoryCreate(generics.CreateAPIView):
    """
    View to create category.

    * Requires category name.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response(
                {"Fail": "Bad Request"},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "Success": f"Category created successfully",
                "New Category": serializer.data
            },
            status=status.HTTP_201_CREATED, headers=headers)


class CategoryDelete(generics.DestroyAPIView):
    """
    View to destroy category.

    * Requires category id.
    * If category is wired to product instance, system will  raise exeption.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        related_product = ProductCategory.objects.filter(category=instance).first()
        print(related_product)
        if related_product is not None:
            return Response(
                {"Restricted": f"Category named {instance.name} has related product."},
            )

        Category.objects.filter(id=instance.id).delete()
        # Don't return super().destroy(request, *args, **kwargs)
        return Response(
            {"Success": f"Category named {instance.name} deleted successfully"},
        )

class ProductCreate(generics.CreateAPIView):
    """
    View to create product and related categories

    * May add many categories at the same time.
    """
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # print(serializer.data)
        if not serializer.is_valid(raise_exception=False):
            return Response(
                {"Fail": "blablal"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # print(serializer)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "Success": f"Product created successfully",
                "New Product": serializer.data
            },
            status=status.HTTP_201_CREATED, headers=headers)


class ProductUpdate(generics.UpdateAPIView):
    """
    View to update product

    * Requires product id.
    """
    queryset = Product.objects.all()
    serializer_class = ProductUpdateSerializer

class ProductDelete(generics.DestroyAPIView):
    """
    View to destroy product

    * Requires product id.
    * Marks as deleted product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductDeleteSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        Product.objects.filter(id=instance.id).update(is_deleted=True)

        return Response(
            {"Success": f"Product named {instance.title} marked as deleted"},
        )

class ProductSearchList(generics.ListAPIView):
    """
    View to search products.

    * Product title
    * Category id
    * Category name
    """
    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_published']
    search_fields = ['title', 'categories__id', 'categories__name']

class ProductFilterList(generics.ListAPIView):
    """
    View to filter by price range.

    * Minimal price
    * Maximal price
    """
    serializer_class = ProductUpdateSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Product.objects.filter(is_deleted=False,
                                      price__range=(self.kwargs['min_price'],
                                                    self.kwargs['max_price']
                                                    ))

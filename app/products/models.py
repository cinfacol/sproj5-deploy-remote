from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from inventario.models import Inventory
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField


class Category(MPTTModel):

    name = models.CharField(
        max_length=100,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("nombre de categoria"),
        help_text=_("format: required, max-100"),
    )
    slug = models.SlugField(
        max_length=150,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("slug"),
        help_text=_(
            "format: required, letters, numbers, underscore, or hyphens"
        ),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("activo"),
        help_text=_("format: true=category visible"),
    )

    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        blank=True,
        unique=False,
        verbose_name=_("categoria padre"),
        help_text=_("format: not required"),
    )

    """ def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug]) """

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("categoria")
        verbose_name_plural = _("product categories")

    def __str__(self):
        return self.name


class Brand(models.Model):

    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("nombre de marca"),
        help_text=_("format: required, unique, max-255"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("brand visibility"),
        help_text=_("format: true=brand visible"),
    )

    def __str__(self):
        return self.name


class Type(models.Model):

    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("tipo de producto"),
        help_text=_("format: required, unique, max-255"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("producto activo"),
        help_text=_("format: true=product visible"),
    )

    def __str__(self):
        return self.name


class Attribute(models.Model):

    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("product attribute name"),
        help_text=_("format: required, unique, max-255"),
    )
    description = models.TextField(
        unique=False,
        null=False,
        blank=False,
        help_text=_("format: required"),
    )

    def __str__(self):
        return self.name


class AttributeValue(models.Model):

    attribute = models.ForeignKey(
        Attribute,
        related_name="attribute",
        on_delete=models.PROTECT,
    )
    attribute_value = models.CharField(
        max_length=255,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("attribute value"),
        help_text=_("format: required, max-255"),
    )

    def __str__(self):
        return f"{self.attribute.name} : {self.attribute_value}"


class Product(models.Model):

    name = models.CharField(
        max_length=255,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("nombre"),
        help_text=_("format: required, max-255"),
    )
    slug = models.SlugField(
        max_length=255,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("Slug"),
        help_text=_(
            "format: required, letters, numbers, underscores or hyphens"
        ),
    )
    web_id = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("ID Web"),
        help_text=_("numero de referencia"),
    )
    inventory = models.ForeignKey(
        Inventory, related_name="products", on_delete=models.CASCADE, null=True, blank=True
    )
    category = TreeManyToManyField(Category, verbose_name="category")
    brand = models.ForeignKey(
        Brand, related_name=_("brand"), on_delete=models.PROTECT
    )
    type = models.ForeignKey(
        Type, verbose_name=_("Product Type"), on_delete=models.CASCADE)
    attribute = models.ManyToManyField(
        Attribute, related_name=_("attributes"))
    description = models.TextField(
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("descripcion"),
        help_text=_("format: required"),
    )
    retail_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("precio al detalle"),
        help_text=_("format: maximum price 9.999.999.99"),
        error_messages={
            "name": {
                "max_length": _("the price must be between 0 and 9.999.999.99."),
            },
        },
    )
    store_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("precio regular"),
        help_text=_("format: maximum price 9.999.999.99"),
        error_messages={
            "name": {
                "max_length": _("the price must be between 0 and 9.999.999.99."),
            },
        },
    )
    percent_discount_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        unique=False,
        null=True,
        blank=True,
        verbose_name=_("descuento %"),
        help_text=_("format: maximum value 99.99"),
        error_messages={
            "name": {
                "max_length": _("the value must be between 0 and 99.99."),
            },
        },
    )
    discount_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        unique=False,
        null=True,
        blank=True,
        verbose_name=_("precio oferta"),
        help_text=_("format: maximum price 9.999.999.99"),
        error_messages={
            "name": {
                "max_length": _("the price must be between 0 and 9.999.999.99."),
            },
        },
    )
    weight = models.FloatField(
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("peso del producto"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("activo"),
        help_text=_("format: true=product visible"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("fecha creacion"),
        help_text=_("format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("actualizado"),
        help_text=_("format: Y-m-d H:M:S"),
    )

    def get_absolute_url(self):
        return reverse("product:product_detail", kwargs={"pk": self.pk})

    def get_categories(self):
        return ', '.join([str(c) for c in self.category.all()])

    def get_price(self):
        if self.discount_price:
            return self.discount_price
        else:
            return self.store_price

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name


class Media(models.Model):

    image = models.ImageField(
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("imagen"),
        upload_to="images/",
        default="images/default.png",
        help_text=_("format: required, default-default.png"),
    )
    alt_text = models.CharField(
        max_length=255,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("texto alternativo"),
        help_text=_("format: required, max-255"),
    )
    product = models.ForeignKey(
        Product, related_name='imagenes', on_delete=models.CASCADE)
    is_featured = models.BooleanField(
        default=False,
        verbose_name=_("destacado"),
        help_text=_("format: default=false, true=default image"),
    )
    default = models.BooleanField(
        default=False,
        verbose_name=_("por defecto"),
        help_text=_("format: default=false, true=default image"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("creado desde"),
        help_text=_("format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("actualizado"),
        help_text=_("format: Y-m-d H:M:S"),
    )

    def get_absolute_url(self):
        return reverse("products:products/product_detail", args=[self.slug])

    class Meta:
        verbose_name = _("product image")
        verbose_name_plural = _("product images")
        ordering = ('created_at',)

    def __str__(self):
        return self.alt_text

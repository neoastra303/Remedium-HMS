from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class InventoryItem(models.Model):
    CATEGORY_CHOICES = [
        ('MEDICAL_SUPPLIES', 'Medical Supplies'),
        ('PHARMACEUTICALS', 'Pharmaceuticals'),
        ('EQUIPMENT', 'Medical Equipment'),
        ('CONSUMABLES', 'Consumables'),
        ('SURGICAL_INSTRUMENTS', 'Surgical Instruments'),
        ('LABORATORY', 'Laboratory Supplies'),
        ('OFFICE_SUPPLIES', 'Office Supplies'),
        ('MAINTENANCE', 'Maintenance Supplies'),
        ('PPE', 'Personal Protective Equipment'),
        ('OTHER', 'Other'),
    ]
    
    UNIT_CHOICES = [
        ('PIECE', 'Piece'),
        ('BOX', 'Box'),
        ('PACK', 'Pack'),
        ('BOTTLE', 'Bottle'),
        ('VIAL', 'Vial'),
        ('TUBE', 'Tube'),
        ('KG', 'Kilogram'),
        ('GRAM', 'Gram'),
        ('LITER', 'Liter'),
        ('ML', 'Milliliter'),
        ('SET', 'Set'),
        ('OTHER', 'Other'),
    ]
    
    class Meta:
        app_label = 'inventory'
        permissions = [
            ('inventory_view_inventoryitem', 'Can view inventory item'),
            ('inventory_add_inventoryitem', 'Can add inventory item'),
            ('inventory_change_inventoryitem', 'Can change inventory item'),
            ('inventory_delete_inventoryitem', 'Can delete inventory item'),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gte=0),
                name='inventory_quantity_non_negative'
            ),
            models.CheckConstraint(
                check=models.Q(reorder_level__gte=0),
                name='inventory_reorder_level_non_negative'
            ),
        ]

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Name of the inventory item"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        help_text="Category of the inventory item"
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        help_text="Current quantity in stock"
    )
    unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        help_text="Unit of measurement"
    )
    reorder_level = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Minimum quantity before reordering"
    )
    cost_per_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Cost per unit"
    )
    supplier = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Supplier name"
    )
    expiry_date = models.DateField(
        blank=True,
        null=True,
        help_text="Expiry date for perishable items"
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        help_text="Last updated timestamp"
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        help_text="Date when item was added to inventory"
    )

    def clean(self):
        super().clean()
        
        # Validate expiry date is not in the past for new items
        if self.expiry_date and self.expiry_date < timezone.now().date():
            if not self.pk:  # New item
                raise ValidationError({
                    'expiry_date': 'Cannot add expired items to inventory.'
                })
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    @property
    def needs_reorder(self):
        """Check if item needs to be reordered."""
        return self.quantity <= self.reorder_level
    
    @property
    def is_expired(self):
        """Check if item is expired."""
        if self.expiry_date:
            from django.utils import timezone
            return self.expiry_date < timezone.now().date()
        return False
    
    @property
    def total_value(self):
        """Calculate total value of stock."""
        if self.cost_per_unit:
            return self.quantity * self.cost_per_unit
        return None
    
    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

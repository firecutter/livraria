from django.contrib import admin
from django.utils import timezone

from .models import Book, Loan


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Configuração do Book no Django Admin."""

    list_display = ("title", "author", "isbn", "copies_total", "copies_available")
    search_fields = ("title", "author", "isbn")
    readonly_fields = ("created_at",)


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    """Configuração do Loan no Django Admin."""

    list_display = ("book", "user", "borrowed_at", "due_date", "returned_at", "_is_overdue")
    list_filter = ("returned_at",)
    search_fields = ("book__title", "user__username")
    actions = ("marcar_como_devolvido",)

    @admin.display(boolean=True, description="Atrasado")
    def _is_overdue(self, obj):
        return obj.is_overdue

    @admin.action(description="Marcar como devolvido")
    def marcar_como_devolvido(self, request, queryset):
        updated = 0
        now = timezone.now()

        for loan in queryset.filter(returned_at__isnull=True):
            loan.returned_at = now
            loan.save(update_fields=["returned_at"])
            updated += 1

        self.message_user(request, f"{updated} empréstimo(s) marcados como devolvidos.")

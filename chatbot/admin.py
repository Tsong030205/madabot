from django.contrib import admin
from .models import FAQ, Reservation, Destination, BudgetEstimate

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'language', 'created_at')
    list_filter = ('language',)
    search_fields = ('question', 'keywords', 'answer')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('destination', 'email', 'start_date', 'end_date', 'num_people', 'language', 'status', 'created_at')
    list_filter = ('language', 'status')
    search_fields = ('destination', 'email')

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'language', 'created_at')
    list_filter = ('language',)
    search_fields = ('name', 'description')

@admin.register(BudgetEstimate)
class BudgetEstimateAdmin(admin.ModelAdmin):
    list_display = ('destination', 'duration_days', 'num_people', 'accommodation_type', 'estimated_cost', 'language', 'created_at')
    list_filter = ('language', 'accommodation_type')
    search_fields = ('destination', 'email')

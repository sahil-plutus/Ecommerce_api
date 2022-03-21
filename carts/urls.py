from django.urls import path, include
from . import views

urlpatterns = [
    path('cart/', views.CartView.as_view()),
    path('orders/', views.OrderAPI.as_view()),
    path('payment/', views.PaymentAPI.as_view()),
    path('webhook/', views.stripe_webhook, name = "stripe_webhook"),
    path('payment_success/', views.PaymentSuccess.as_view(), name = "payment_success"),
    path('payment_cancel/', views.PaymentCancel.as_view(), name = "payment_cancel"),
    path('show_invoice/', views.ShowInvoice.as_view(), name = "show_cancel"),
    path('invoice_download/', views.DownloadInvoice.as_view(), name = "download_invoice"),
    path('share_invoice/', views.ShareInvoice.as_view(), name = "share_invoice"),
]

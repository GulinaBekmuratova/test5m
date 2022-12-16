from django.urls import path,include
from Watches import views
from rest_framework.routers import SimpleRouter



ROUTER = SimpleRouter()
ROUTER.register('watch-crud', views.WatchViewSet)
ROUTER.register('category-crud', views.CategoryViewSet)
ROUTER.register('photo-crud', views.PhotoViewSet)
ROUTER.register('review-crud', views.ReviewViewSet)


urlpatterns = [
    path('watches/<int:cat_id>/', views.WatchListApiView.as_view(), name='watch list'),
    path('', include(ROUTER.urls)),
    path('category/', views.CategoryListApiView.as_view()),
    path('category/<int:pk>/', views.CategoryDetailAPIView.as_view()),
    path('reviews/', views.ReviewListAPIView.as_view()),
    path('reviews/<int:pk>/', views.ReviewItemUpdateDeleteAPIView.as_view())
]
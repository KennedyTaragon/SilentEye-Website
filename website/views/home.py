from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest
from ..models import SiteConfig, Post, Service, Product, Client, Testimonial, Benefit, TeamMember
from ..forms import ContactForm


def homepage_view(request):
    # Retrieve SiteConfig (Singleton)
    site_config = SiteConfig.objects.first()
    
    # Retrieve all ordered Benefits
    benefits = Benefit.objects.all().order_by('order')
    
    # Retrieve active and ordered Services
    services = Service.objects.filter(is_active=True).order_by('order')
    
    # Retrieve active and ordered Team Members
    team_members = TeamMember.objects.filter(is_active=True).order_by('order')
    
    # Testimonials
    testimonials = Testimonial.objects.all()
    
    # Latest Posts (Optimized and Ordered)
    latest_posts = Post.objects.filter(is_published=True) \
        .select_related('author') \
        .order_by('-published_date')[:3]
    
    # Featured Products (Optimized, Filtered, and Ordered)
    featured_products = Product.objects.filter(is_featured=True) \
        .select_related('category') \
        .order_by('order')
        
    # Client Logos (Fetching all client logos for the logo slider)
    client_logos = Client.objects.all()

    context = {
        'site_config': site_config,
        'latest_posts': latest_posts,
        'services': services,
        'featured_products': featured_products,
        'client_logos': client_logos, # Renamed from featured_projects for clarity
        'testimonials': testimonials,
        'benefits': benefits,
        'team_members': team_members,
        'form': ContactForm(),  # Add contact form to context
    }
    return render(request, 'website/index.html', context)


def contact_form_view(request):
    """
    Handle contact form submissions
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the contact message to database
            contact_message = form.save()
            
            # Add success message
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            
            # Redirect to homepage with contact anchor and success message
            return redirect('website:home') + '#contact'
        else:
            # Add error message
            messages.error(request, 'Please correct the errors below and try again.')
    else:
        # This shouldn't happen - contact form should always be POST
        return redirect('website:home')
    
    # If we get here, the form had errors - redirect to home and let messages display
    return redirect('website:home')
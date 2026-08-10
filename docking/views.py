from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q
from django.views.generic import ListView, TemplateView, FormView
from .models import PDBQuery, AMP, TargetProtein, Dock
import os

def EnterPage(request):
    return render(request, "search.html")

def IndexPage(request):
    return render(request, "index.html")

def AboutUsPage(request):
    return render(request, "about_us.html")

class ContactView(generic.TemplateView):
    """Contact section of the AMPdb tool."""
    model = PDBQuery
    template_name = "contact.html"

def TutorialPage(request):
    return render(request, 'tutorial.html')

def search_view(request):
    return render(request, "search.html", {
        "targets": TargetProtein.objects.all(),
        "proteins": AMP.objects.all()
    })

def protein(request, proteins_id):
    protein = get_object_or_404(AMP, pk=proteins_id)
    target_protein = protein.target_protein
    dock = Dock.objects.filter(amp=protein, target_protein=target_protein)
    return render(request, "protein.html", {
        "protein": protein,
        "dock": dock,
    })


def create_protein(request):
    if request.method == 'POST':
        protein_id = request.POST.get('protein_id')
        protein_name = request.POST.get('protein_name')
        score = request.POST.get('score')
        sequence = request.POST.get('sequence')
        target_protein_id = request.POST.get('target_id')
        
        try:
            protein = AMP.objects.get(id=protein_id)
            protein.target_protein_id = target_protein_id
            protein.save()
            
            target_protein = TargetProtein.objects.get(id=target_protein_id)
            target_protein_name = target_protein.target_protein + '_' + protein.pdb_name[2:]
            
            dock_instances = Dock.objects.filter(dock__contains=target_protein_name)
            for dock_instance in dock_instances:
                dock_instance.target_protein.add(target_protein)
            
            redirect_url = reverse('protein', kwargs={'proteins_id': protein_id})
            return redirect(redirect_url)
        except AMP.DoesNotExist:
            messages.error(request, 'Protein not found')
            return redirect('create_protein')  # Redirect to a relevant page
        except TargetProtein.DoesNotExist:
            messages.error(request, 'Target Protein not found')
            return redirect('create_protein')  # Redirect to a relevant page
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('create_protein')  # Redirect to a relevant page
    else:
        return HttpResponse('Invalid request method')


def StatsPage(request):
    def to_float(v):
        try:
            return float(v)
        except (TypeError, ValueError):
            return 0.0

    amps = AMP.objects.all().order_by('id')
    data = []
    for a in amps:
        data.append({
            "amp": a.amp_no,
            "name": a.name,
            "Molecular Weight": round(to_float(a.molecular_weight), 3),
            "Length": to_float(a.length),
            "Net Charge": round(to_float(a.charge), 3),
            "Isoelectric Point": round(to_float(a.isoelectric_point), 3),
            "Aliphatic Index": round(to_float(a.aliphatic_index), 3),
            "Instability Index": round(to_float(a.instability_index), 3),
            "Boman Index": round(to_float(a.boman_index), 3),
            "Hydrophobic Moment": round(to_float(a.hydrophobic_moment), 3),
            "Amphipathicity": round(to_float(str(a.hp).replace('%', '')), 2),
        })

    return render(request, 'stats.html', {"amp_data": data})
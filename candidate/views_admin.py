# candidate/views_admin.py
# Brought to you by We Vote. Be good.
# -*- coding: UTF-8 -*-

from .controllers import candidates_import_from_sample_file
from .models import CandidateCampaign
from .serializers import CandidateCampaignSerializer
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages
from django.shortcuts import render
from election.models import Election
from exception.models import handle_record_found_more_than_one_exception,\
    handle_record_not_found_exception, handle_record_not_saved_exception
from rest_framework.views import APIView
from rest_framework.response import Response
import wevote_functions.admin
from wevote_functions.models import convert_to_int, positive_value_exists


logger = wevote_functions.admin.get_logger(__name__)


# This page does not need to be protected.
# NOTE: login_required() throws an error. Needs to be figured out if we ever want to secure this page.
class ExportCandidateCampaignDataView(APIView):
    def get(self, request, format=None):
        candidate_campaign_list = CandidateCampaign.objects.all()
        serializer = CandidateCampaignSerializer(candidate_campaign_list, many=True)
        return Response(serializer.data)


def candidates_import_from_sample_file_view(request):
    """
    This gives us sample organizations, candidate campaigns, and positions for testing
    :return:
    """
    # We are importing candidate_campaigns data (and not politician data) because all we are doing is making sure we
    #  sync to the same We Vote ID. This is critical so we can link Positions to Organization & Candidate Campaign.
    # At this point (June 2015) we assume the politicians have been imported from Google Civic. We aren't assigning
    # the politicians a We Vote id, but instead use their full name as the identifier
    candidates_import_from_sample_file(request, False)

    messages.add_message(request, messages.INFO, 'Candidates imported.')

    return HttpResponseRedirect(reverse('import_export:import_export_index', args=()))


# @login_required()  # Commented out while we are developing login process
def candidate_list_view(request):
    messages_on_stage = get_messages(request)
    google_civic_election_id = request.GET.get('google_civic_election_id', 0)

    try:
        candidate_list = CandidateCampaign.objects.order_by('candidate_name')
        if positive_value_exists(google_civic_election_id):
            candidate_list = candidate_list.filter(google_civic_election_id=google_civic_election_id)
    except CandidateCampaign.DoesNotExist:
        # This is fine, create new
        pass

    election_list = Election.objects.order_by('-election_day_text')

    template_values = {
        'messages_on_stage': messages_on_stage,
        'candidate_list': candidate_list,
        'election_list': election_list,
        'google_civic_election_id': google_civic_election_id,
    }
    return render(request, 'candidate/candidate_list.html', template_values)


# @login_required()  # Commented out while we are developing login process
def candidate_new_view(request):
    messages_on_stage = get_messages(request)
    template_values = {
        'messages_on_stage': messages_on_stage,
    }
    return render(request, 'candidate/candidate_edit.html', template_values)


# @login_required()  # Commented out while we are developing login process
def candidate_edit_view(request, candidate_id):
    messages_on_stage = get_messages(request)
    candidate_id = convert_to_int(candidate_id)
    candidate_on_stage_found = False
    candidate_on_stage = CandidateCampaign()
    try:
        candidate_on_stage = CandidateCampaign.objects.get(id=candidate_id)
        candidate_on_stage_found = True
    except CandidateCampaign.MultipleObjectsReturned as e:
        handle_record_found_more_than_one_exception(e, logger=logger)
    except CandidateCampaign.DoesNotExist:
        # This is fine, create new
        pass

    if candidate_on_stage_found:
        template_values = {
            'messages_on_stage': messages_on_stage,
            'candidate': candidate_on_stage,
        }
    else:
        template_values = {
            'messages_on_stage': messages_on_stage,
        }
    return render(request, 'candidate/candidate_edit.html', template_values)


# @login_required()  # Commented out while we are developing login process
def candidate_edit_process_view(request):
    """
    Process the new or edit candidate forms
    :param request:
    :return:
    """
    candidate_id = convert_to_int(request.POST['candidate_id'])
    candidate_name = request.POST['candidate_name']
    twitter_handle = request.POST['twitter_handle']
    candidate_website = request.POST['candidate_website']

    # Check to see if this candidate is already being used anywhere
    candidate_on_stage_found = False
    candidate_on_stage = CandidateCampaign()
    try:
        candidate_query = CandidateCampaign.objects.filter(id=candidate_id)
        if len(candidate_query):
            candidate_on_stage = candidate_query[0]
            candidate_on_stage_found = True
    except Exception as e:
        handle_record_not_found_exception(e, logger=logger)

    try:
        if candidate_on_stage_found:
            # Update
            candidate_on_stage.candidate_name = candidate_name
            candidate_on_stage.twitter_handle = twitter_handle
            candidate_on_stage.candidate_website = candidate_website
            candidate_on_stage.save()
            messages.add_message(request, messages.INFO, 'CandidateCampaign updated.')
        else:
            # Create new
            candidate_on_stage = CandidateCampaign(
                candidate_name=candidate_name,
                twitter_handle=twitter_handle,
                candidate_website=candidate_website,
            )
            candidate_on_stage.save()
            messages.add_message(request, messages.INFO, 'New candidate saved.')
    except Exception as e:
        handle_record_not_saved_exception(e, logger=logger)
        messages.add_message(request, messages.ERROR, 'Could not save candidate.')

    return HttpResponseRedirect(reverse('candidate:candidate_list', args=()))


# @login_required()  # Commented out while we are developing login process()
def candidate_summary_view(request, candidate_id):
    messages_on_stage = get_messages(request)
    candidate_id = convert_to_int(candidate_id)
    candidate_on_stage_found = False
    candidate_on_stage = CandidateCampaign()
    try:
        candidate_on_stage = CandidateCampaign.objects.get(id=candidate_id)
        candidate_on_stage_found = True
    except CandidateCampaign.MultipleObjectsReturned as e:
        handle_record_found_more_than_one_exception(e, logger=logger)
    except CandidateCampaign.DoesNotExist:
        # This is fine, create new
        pass

    if candidate_on_stage_found:
        template_values = {
            'messages_on_stage': messages_on_stage,
            'candidate': candidate_on_stage,
        }
    else:
        template_values = {
            'messages_on_stage': messages_on_stage,
        }
    return render(request, 'candidate/candidate_summary.html', template_values)

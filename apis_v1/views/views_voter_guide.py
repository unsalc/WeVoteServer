# apis_v1/views/views_voter_guide.py
# Brought to you by We Vote. Be good.
# -*- coding: UTF-8 -*-

from ballot.controllers import choose_election_from_existing_data
from config.base import get_environment_variable
from django.http import HttpResponse
import json
from voter.models import VoterAddress, VoterAddressManager, VoterDeviceLinkManager
from voter_guide.controllers import voter_guide_possibility_retrieve_for_api, voter_guide_possibility_save_for_api, \
    voter_guide_save_for_api, \
    voter_guides_followed_retrieve_for_api, voter_guides_ignored_retrieve_for_api, voter_guides_retrieve_for_api, \
    voter_guides_followed_by_organization_retrieve_for_api, \
    voter_guide_followers_retrieve_for_api, \
    voter_guides_to_follow_retrieve_for_api, voter_guides_upcoming_retrieve_for_api
import wevote_functions.admin
from wevote_functions.functions import convert_to_int, get_maximum_number_to_retrieve_from_request, \
    get_voter_device_id, positive_value_exists

logger = wevote_functions.admin.get_logger(__name__)

WE_VOTE_SERVER_ROOT_URL = get_environment_variable("WE_VOTE_SERVER_ROOT_URL")


def voter_guide_possibility_retrieve_view(request):  # voterGuidePossibilityRetrieve
    """
    Retrieve a previously saved website that may contain a voter guide (voterGuidePossibilityRetrieve)
    :param request:
    :return:
    """
    voter_device_id = get_voter_device_id(request)  # We standardize how we take in the voter_device_id
    voter_guide_possibility_url = request.GET.get('voter_guide_possibility_url', '')
    return voter_guide_possibility_retrieve_for_api(voter_device_id=voter_device_id,
                                                    voter_guide_possibility_url=voter_guide_possibility_url)


def voter_guide_possibility_save_view(request):  # voterGuidePossibilitySave
    """
    Save a website that may contain a voter guide (voterGuidePossibilitySave)
    :param request:
    :return:
    """
    voter_device_id = get_voter_device_id(request)  # We standardize how we take in the voter_device_id
    voter_guide_possibility_url = request.GET.get('voter_guide_possibility_url', '')
    return voter_guide_possibility_save_for_api(voter_device_id=voter_device_id,
                                                voter_guide_possibility_url=voter_guide_possibility_url)


def voter_guides_followed_retrieve_view(request):  # voterGuidesFollowedRetrieve
    voter_device_id = get_voter_device_id(request)  # We standardize how we take in the voter_device_id
    maximum_number_to_retrieve = get_maximum_number_to_retrieve_from_request(request)
    return voter_guides_followed_retrieve_for_api(voter_device_id=voter_device_id,
                                                  maximum_number_to_retrieve=maximum_number_to_retrieve)


def voter_guides_followed_by_organization_retrieve_view(request):  # voterGuidesFollowedByOrganizationRetrieve
    voter_linked_organization_we_vote_id = request.GET.get('organization_we_vote_id', '')
    filter_by_this_google_civic_election_id = request.GET.get('filter_by_this_google_civic_election_id', '')
    voter_device_id = get_voter_device_id(request)  # We standardize how we take in the voter_device_id
    maximum_number_to_retrieve = get_maximum_number_to_retrieve_from_request(request)
    return voter_guides_followed_by_organization_retrieve_for_api(
        voter_device_id,
        voter_linked_organization_we_vote_id=voter_linked_organization_we_vote_id,
        filter_by_this_google_civic_election_id=filter_by_this_google_civic_election_id,
        maximum_number_to_retrieve=maximum_number_to_retrieve)


def voter_guide_followers_retrieve_view(request):  # voterGuideFollowersRetrieve
    organization_we_vote_id = request.GET.get('organization_we_vote_id', '')
    voter_device_id = get_voter_device_id(request)  # We standardize how we take in the voter_device_id
    maximum_number_to_retrieve = get_maximum_number_to_retrieve_from_request(request)
    return voter_guide_followers_retrieve_for_api(
        voter_device_id, organization_we_vote_id=organization_we_vote_id,
        maximum_number_to_retrieve=maximum_number_to_retrieve)


def voter_guide_save_view(request):  # voterGuideSave
    voter_device_id = get_voter_device_id(request)  # We standardize how we take in the voter_device_id
    voter_guide_we_vote_id = request.GET.get('voter_guide_we_vote_id', '')
    google_civic_election_id = convert_to_int(request.GET.get('google_civic_election_id', 0))
    return voter_guide_save_for_api(voter_device_id=voter_device_id,
                                    voter_guide_we_vote_id=voter_guide_we_vote_id,
                                    google_civic_election_id=google_civic_election_id)


def voter_guides_ignored_retrieve_view(request):  # voterGuidesIgnoredRetrieve
    voter_device_id = get_voter_device_id(request)  # We standardize how we take in the voter_device_id
    maximum_number_to_retrieve = get_maximum_number_to_retrieve_from_request(request)
    return voter_guides_ignored_retrieve_for_api(voter_device_id=voter_device_id,
                                                 maximum_number_to_retrieve=maximum_number_to_retrieve)


def voter_guides_retrieve_view(request):  # voterGuidesRetrieve
    voter_device_id = get_voter_device_id(request)  # We standardize how we take in the voter_device_id
    organization_we_vote_id = request.GET.get('organization_we_vote_id', '')
    voter_we_vote_id = request.GET.get('voter_we_vote_id', '')
    maximum_number_to_retrieve = get_maximum_number_to_retrieve_from_request(request)
    return voter_guides_retrieve_for_api(voter_device_id=voter_device_id,
                                         organization_we_vote_id=organization_we_vote_id,
                                         voter_we_vote_id=voter_we_vote_id,
                                         maximum_number_to_retrieve=maximum_number_to_retrieve)


def voter_guides_to_follow_retrieve_view(request):  # voterGuidesToFollowRetrieve
    """
    Retrieve a list of voter_guides that a voter might want to follow (voterGuidesToFollow)
    :param request:
    :return:
    """
    voter_device_id = get_voter_device_id(request)  # We standardize how we take in the voter_device_id
    kind_of_ballot_item = request.GET.get('kind_of_ballot_item', '')
    ballot_item_we_vote_id = request.GET.get('ballot_item_we_vote_id', '')
    google_civic_election_id = convert_to_int(request.GET.get('google_civic_election_id', 0))
    search_string = request.GET.get('search_string', '')
    use_test_election = positive_value_exists(request.GET.get('use_test_election', False))
    maximum_number_to_retrieve = get_maximum_number_to_retrieve_from_request(request)
    start_retrieve_at_this_number = request.GET.get('start_retrieve_at_this_number', 0)
    filter_voter_guides_by_issue = positive_value_exists(request.GET.get('filter_voter_guides_by_issue', False))
    # If we want to show voter guides associated with election first, but then show more after those are exhausted,
    #  set add_voter_guides_not_from_election to True
    add_voter_guides_not_from_election = request.GET.get('add_voter_guides_not_from_election', False)
    add_voter_guides_not_from_election = positive_value_exists(add_voter_guides_not_from_election)

    if positive_value_exists(ballot_item_we_vote_id):
        # We don't need both ballot_item and google_civic_election_id
        google_civic_election_id = 0
    else:
        if positive_value_exists(use_test_election):
            google_civic_election_id = 2000  # The Google Civic API Test election
        elif positive_value_exists(google_civic_election_id) or google_civic_election_id == 0:  # Why "0" election?
            # If an election was specified, we can skip down to retrieving the voter_guides
            pass
        else:
            # If here we don't have either a ballot_item or a google_civic_election_id.
            # Look in the places we cache google_civic_election_id
            google_civic_election_id = 0
            voter_device_link_manager = VoterDeviceLinkManager()
            voter_device_link_results = voter_device_link_manager.retrieve_voter_device_link(voter_device_id)
            voter_device_link = voter_device_link_results['voter_device_link']
            if voter_device_link_results['voter_device_link_found']:
                voter_id = voter_device_link.voter_id
                voter_address_manager = VoterAddressManager()
                voter_address_results = voter_address_manager.retrieve_address(0, voter_id)
                if voter_address_results['voter_address_found']:
                    voter_address = voter_address_results['voter_address']
                else:
                    voter_address = VoterAddress()
            else:
                voter_address = VoterAddress()
            results = choose_election_from_existing_data(voter_device_link, google_civic_election_id, voter_address)
            google_civic_election_id = results['google_civic_election_id']

        # In order to return voter_guides that are independent of an election or ballot_item, we need to pass in
        # google_civic_election_id as 0

    results = voter_guides_to_follow_retrieve_for_api(voter_device_id, kind_of_ballot_item, ballot_item_we_vote_id,
                                                      google_civic_election_id, search_string,
                                                      start_retrieve_at_this_number, maximum_number_to_retrieve,
                                                      filter_voter_guides_by_issue,
                                                      add_voter_guides_not_from_election)
    return HttpResponse(json.dumps(results['json_data']), content_type='application/json')


def voter_guides_upcoming_retrieve_view(request):  # voterGuidesUpcomingRetrieve
    """
    Retrieve a list of voter_guides that a voter might want to follow (voterGuidesUpcoming)
    :param request:
    :return:
    """
    status = ""
    google_civic_election_id_list = request.GET.get('google_civic_election_id_list', [])

    if positive_value_exists(google_civic_election_id_list):
        if not positive_value_exists(len(google_civic_election_id_list)):
            google_civic_election_id_list = []
    else:
        google_civic_election_id_list = []

    results = voter_guides_upcoming_retrieve_for_api(google_civic_election_id_list=google_civic_election_id_list)
    status += results['status']

    return HttpResponse(json.dumps(results['json_data']), content_type='application/json')

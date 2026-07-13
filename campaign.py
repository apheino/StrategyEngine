"""
Campaign Management System

This module handles campaign definitions, progress tracking, and scenario sequencing.
Campaigns are defined in JSON files in resources/campaigns/ directory.

Campaign JSON Structure:
{
    "id": "campaign_id",
    "name": "Campaign Name",
    "description": "Campaign description",
    "scenarios": [
        {
            "scenario_number": 1,
            "required": true,
            "unlock_condition": null,
            "briefing_override": ["Optional", "Custom briefing text"]
        }
    ],
    "victory_text": ["Campaign complete!", "..."]
}
"""

import json
import os
from pathlib import Path


class Campaign:
    """Represents a campaign with multiple scenarios"""
    
    def __init__(self, campaign_data):
        """
        Initialize a campaign from JSON data
        
        Args:
            campaign_data: Dictionary loaded from campaign JSON file
        """
        self.id = campaign_data['id']
        self.name = campaign_data['name']
        self.description = campaign_data.get('description', '')
        self.scenarios = campaign_data['scenarios']
        self.victory_text = campaign_data.get('victory_text', [])
        self.current_index = 0
        self.completed_scenarios = set()
    
    def get_current_scenario(self):
        """
        Get the current scenario number
        
        Returns:
            int: Scenario number or None if campaign complete
        """
        if self.current_index >= len(self.scenarios):
            return None
        
        return self.scenarios[self.current_index]['scenario_number']
    
    def get_next_scenario(self):
        """
        Get the next scenario number after completing current
        
        Returns:
            int: Next scenario number or None if campaign complete
        """
        next_index = self.current_index + 1
        if next_index >= len(self.scenarios):
            return None
        
        return self.scenarios[next_index]['scenario_number']
    
    def mark_scenario_complete(self, scenario_number):
        """
        Mark a scenario as completed and advance campaign
        
        Args:
            scenario_number: The scenario that was completed
        """
        self.completed_scenarios.add(scenario_number)
        
        # Advance to next scenario if current one was completed
        if self.current_index < len(self.scenarios):
            current = self.scenarios[self.current_index]['scenario_number']
            if current == scenario_number:
                self.current_index += 1
    
    def is_complete(self):
        """
        Check if all campaign scenarios are completed
        
        Returns:
            bool: True if campaign is complete
        """
        return self.current_index >= len(self.scenarios)
    
    def get_scenario_info(self, scenario_number):
        """
        Get campaign-specific info for a scenario
        
        Args:
            scenario_number: The scenario to get info for
            
        Returns:
            dict: Scenario info or None if not in campaign
        """
        for scenario in self.scenarios:
            if scenario['scenario_number'] == scenario_number:
                return scenario
        return None
    
    def get_progress_text(self):
        """
        Get text describing campaign progress
        
        Returns:
            str: Progress description like "Scenario 2 of 3"
        """
        if self.is_complete():
            return f"Campaign Complete: {len(self.scenarios)}/{len(self.scenarios)}"
        
        return f"Scenario {self.current_index + 1} of {len(self.scenarios)}"


def load_campaign(campaign_id):
    """
    Load a campaign from JSON file
    
    Args:
        campaign_id: Campaign identifier (filename without .json)
        
    Returns:
        Campaign: Loaded campaign object or None if not found
    """
    campaign_path = Path('resources/campaigns') / f'{campaign_id}.json'
    
    if not campaign_path.exists():
        print(f"Campaign file not found: {campaign_path}")
        return None
    
    try:
        with open(campaign_path, 'r') as f:
            data = json.load(f)
        
        return Campaign(data)
    except Exception as e:
        print(f"Error loading campaign {campaign_id}: {e}")
        return None


def get_available_campaigns():
    """
    Get list of all available campaigns
    
    Returns:
        list: List of tuples (campaign_id, campaign_name, description)
    """
    campaigns = []
    campaign_dir = Path('resources/campaigns')
    
    if not campaign_dir.exists():
        return campaigns
    
    for campaign_file in campaign_dir.glob('*.json'):
        try:
            with open(campaign_file, 'r') as f:
                data = json.load(f)
            
            campaigns.append((
                data['id'],
                data['name'],
                data.get('description', '')
            ))
        except Exception as e:
            print(f"Error reading campaign {campaign_file}: {e}")
    
    return campaigns


# Global current campaign instance
current_campaign = None


def start_campaign(campaign_id):
    """
    Start a new campaign
    
    Args:
        campaign_id: ID of campaign to start
        
    Returns:
        Campaign: The started campaign or None if load failed
    """
    global current_campaign
    current_campaign = load_campaign(campaign_id)
    return current_campaign


def get_current_campaign():
    """
    Get the currently active campaign
    
    Returns:
        Campaign: Current campaign or None
    """
    return current_campaign


def end_campaign():
    """End the current campaign"""
    global current_campaign
    current_campaign = None

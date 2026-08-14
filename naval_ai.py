"""
Enhanced AI for Caribbean Naval Warfare
Provides intelligent enemy behavior including:
- Fleet coordination
- Tactical positioning
- Target prioritization
- Defensive formations
- Adaptive strategies
"""

import random
from typing import List, Tuple, Optional


class NavalAI:
    """Enhanced AI for naval combat"""
    
    def __init__(self, difficulty=5):
        """
        Initialize AI with difficulty level
        difficulty: 1-10, affects decision quality and reaction speed
        """
        self.difficulty = difficulty
        self.tactics = {
            "aggressive": 0.7 if difficulty > 5 else 0.5,
            "defensive": 0.3 if difficulty > 5 else 0.5,
            "coordinated": difficulty > 3
        }
    
    def evaluate_target_priority(self, unit, targets, game_state):
        """
        Evaluate and prioritize targets based on:
        - Threat level (damage potential)
        - Health (finish weak targets)
        - Strategic value
        - Distance
        """
        scored_targets = []
        
        for target in targets:
            score = 0
            
            # Prioritize low health targets (can be finished off)
            health_percent = target.current_hp / target.max_hp
            if health_percent < 0.3:
                score += 50  # High priority - finish them!
            elif health_percent < 0.6:
                score += 25
            
            # Prioritize high-damage threats
            if hasattr(target, 'attack'):
                score += target.attack * 2
            
            # Distance factor (closer = higher priority)
            distance = self.get_distance(unit.position, target.position)
            max_range = unit.attack_range if hasattr(unit, 'attack_range') else 5
            if distance <= max_range:
                score += 30  # In range!
            else:
                score -= distance * 2  # Penalty for distance
            
            # Unit type bonuses
            if target.unit_type == "ship_of_the_line":
                score += 30  # High-value target
            elif target.unit_type == "frigate":
                score += 25  # Artillery threat
            
            # Random variation for unpredictability
            score += random.randint(-10, 10)
            
            scored_targets.append((target, score))
        
        # Sort by score (highest first)
        scored_targets.sort(key=lambda x: x[1], reverse=True)
        return [t[0] for t in scored_targets]
    
    def decide_action(self, unit, visible_enemies, visible_allies, game_state):
        """
        Decide the best action for this unit
        Returns: ("action_type", parameters)
        """
        if not visible_enemies:
            return ("patrol", self.get_patrol_position(unit, game_state))
        
        # Get prioritized targets
        priority_targets = self.evaluate_target_priority(unit, visible_enemies, game_state)
        best_target = priority_targets[0] if priority_targets else None
        
        if not best_target:
            return ("patrol", self.get_patrol_position(unit, game_state))
        
        # Calculate distance to best target
        distance = self.get_distance(unit.position, best_target.position)
        attack_range = unit.attack_range if hasattr(unit, 'attack_range') else 3
        
        # Decide based on unit health and tactics
        health_percent = unit.current_hp / unit.max_hp
        
        # Retreat if badly damaged and defensive
        if health_percent < 0.25 and self.tactics["defensive"] > 0.5:
            return ("retreat", self.get_retreat_position(unit, visible_enemies, visible_allies))
        
        # Attack if in range
        if distance <= attack_range:
            # Check if should focus fire with allies
            if self.tactics["coordinated"] and self.should_focus_fire(unit, best_target, visible_allies):
                return ("attack", best_target)
            else:
                return ("attack", best_target)
        
        # Move toward target if aggressive
        if self.tactics["aggressive"] > 0.5:
            # Check if should wait for allies
            if self.tactics["coordinated"] and self.should_wait_for_allies(unit, visible_enemies, visible_allies):
                return ("wait", unit.position)
            else:
                return ("move_attack", self.get_approach_position(unit, best_target, attack_range))
        else:
            # Defensive - maintain position or form up
            return ("defensive_position", self.get_defensive_position(unit, visible_allies))
    
    def should_focus_fire(self, unit, target, allies):
        """Determine if allies are also targeting this enemy"""
        if self.difficulty < 5:
            return False
        
        # Count how many allies could also attack this target
        allies_in_range = 0
        for ally in allies:
            if hasattr(ally, 'position') and hasattr(ally, 'attack_range'):
                distance = self.get_distance(ally.position, target.position)
                if distance <= ally.attack_range:
                    allies_in_range += 1
        
        # Focus fire if 2+ units can hit same target
        return allies_in_range >= 2
    
    def should_wait_for_allies(self, unit, enemies, allies):
        """Determine if unit should wait for allies before engaging"""
        if self.difficulty < 6:
            return False
        
        # Check if outnumbered
        nearby_enemies = sum(1 for e in enemies if self.get_distance(unit.position, e.position) < 8)
        nearby_allies = sum(1 for a in allies if self.get_distance(unit.position, a.position) < 8)
        
        # Wait if outnumbered 2:1 or worse
        return nearby_enemies > nearby_allies * 2
    
    def get_distance(self, pos1, pos2):
        """Calculate Manhattan distance"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def get_approach_position(self, unit, target, preferred_range):
        """Get position to approach target while maintaining optimal range"""
        ux, uy = unit.position
        tx, ty = target.position
        
        # Calculate direction
        dx = tx - ux
        dy = ty - uy
        
        # Normalize
        distance = max(abs(dx), abs(dy))
        if distance == 0:
            return unit.position
        
        step_x = 1 if dx > 0 else (-1 if dx < 0 else 0)
        step_y = 1 if dy > 0 else (-1 if dy < 0 else 0)
        
        # Move toward target but maintain preferred_range - 1
        move_distance = min(distance - (preferred_range - 1), 
                           unit.movement if hasattr(unit, 'movement') else 3)
        
        new_x = ux + step_x * move_distance
        new_y = uy + step_y * move_distance
        
        return (new_x, new_y)
    
    def get_retreat_position(self, unit, enemies, allies):
        """Find safe retreat position away from enemies"""
        ux, uy = unit.position
        
        # Calculate average enemy position
        if enemies:
            avg_ex = sum(e.position[0] for e in enemies) / len(enemies)
            avg_ey = sum(e.position[1] for e in enemies) / len(enemies)
            
            # Move away from enemies
            step_x = -1 if avg_ex > ux else (1 if avg_ex < ux else 0)
            step_y = -1 if avg_ey > uy else (1 if avg_ey < uy else 0)
        else:
            step_x, step_y = 0, 0
        
        move_distance = unit.movement if hasattr(unit, 'movement') else 3
        new_x = ux + step_x * move_distance
        new_y = uy + step_y * move_distance
        
        return (new_x, new_y)
    
    def get_defensive_position(self, unit, allies):
        """Get position for defensive formation"""
        if not allies:
            return unit.position
        
        # Form up near allies
        avg_ax = sum(a.position[0] for a in allies) / len(allies)
        avg_ay = sum(a.position[1] for a in allies) / len(allies)
        
        ux, uy = unit.position
        
        # Move toward ally center
        step_x = 1 if avg_ax > ux else (-1 if avg_ax < ux else 0)
        step_y = 1 if avg_ay > uy else (-1 if avg_ay < uy else 0)
        
        move_distance = min(2, unit.movement if hasattr(unit, 'movement') else 3)
        new_x = ux + step_x * move_distance
        new_y = uy + step_y * move_distance
        
        return (new_x, new_y)
    
    def get_patrol_position(self, unit, game_state):
        """Get position for patrol behavior"""
        # Random patrol pattern
        ux, uy = unit.position
        move_distance = unit.movement if hasattr(unit, 'movement') else 3
        
        dx = random.randint(-move_distance, move_distance)
        dy = random.randint(-move_distance, move_distance)
        
        return (ux + dx, uy + dy)
    
    def evaluate_fleet_strategy(self, friendly_units, enemy_units, game_state):
        """
        Evaluate overall fleet strategy
        Returns strategy directive for all units
        """
        if not enemy_units:
            return "patrol"
        
        # Count units and calculate strength
        friendly_count = len(friendly_units)
        enemy_count = len(enemy_units)
        
        friendly_strength = sum(u.current_hp * (u.attack if hasattr(u, 'attack') else 1) 
                               for u in friendly_units)
        enemy_strength = sum(u.current_hp * (u.attack if hasattr(u, 'attack') else 1) 
                            for u in enemy_units)
        
        # Strategic decisions based on strength comparison
        strength_ratio = friendly_strength / enemy_strength if enemy_strength > 0 else 2
        
        if strength_ratio > 1.5:
            return "aggressive"  # We're winning - press the attack
        elif strength_ratio < 0.5:
            return "defensive"  # We're losing - regroup and defend
        else:
            return "balanced"  # Even match - tactical combat
    
    def coordinate_attack(self, friendly_units, target, game_state):
        """
        Coordinate multiple units to attack one target
        Returns list of (unit, action) pairs
        """
        if not self.tactics["coordinated"]:
            return []
        
        actions = []
        for unit in friendly_units:
            distance = self.get_distance(unit.position, target.position)
            attack_range = unit.attack_range if hasattr(unit, 'attack_range') else 3
            
            if distance <= attack_range:
                actions.append((unit, ("attack", target)))
            else:
                move_pos = self.get_approach_position(unit, target, attack_range)
                actions.append((unit, ("move", move_pos)))
        
        return actions


# Pre-configured AI personalities
DIFFICULTY_PRESETS = {
    "easy": NavalAI(difficulty=3),
    "normal": NavalAI(difficulty=5),
    "hard": NavalAI(difficulty=7),
    "expert": NavalAI(difficulty=9),
    "pirate_king": NavalAI(difficulty=10)
}

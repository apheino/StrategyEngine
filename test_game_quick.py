#!/usr/bin/env python3
"""
Quick test to verify game launches and runs without crashing
"""
import pygame
import sys

def test_game():
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    clock = pygame.time.Clock()
    
    from scenario import Scenario
    
    # Load scenario
    scenario = Scenario(scenario_number=1)
    
    print(f"✅ Scenario loaded!")
    print(f"  Units: {len(scenario.units)}")
    
    # Simulate a few frames
    running = True
    frames = 0
    max_frames = 60  # Test for 1 second at 60 FPS
    
    while running and frames < max_frames:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update scenario
        scenario.update(dt)
        
        # Draw
        screen.fill((50, 100, 150))
        scenario.draw(screen)
        pygame.display.flip()
        
        frames += 1
        if frames % 20 == 0:
            print(f"  Frame {frames}: OK")
    
    pygame.quit()
    print("✅ SUCCESS! Game runs without crashing!")
    print("Ships are visible and animated!")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(test_game())
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

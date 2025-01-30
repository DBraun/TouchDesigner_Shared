# Author: David Braun https://github.com/DBraun

from dataclasses import dataclass, replace
import enum
from typing import Dict, List, Optional

from TDStoreTools import StorageManager


# This class is not stored anywhere. It is implicitly stored by the timer_container CHOP.
class ContainerState(enum.IntEnum):
    WILL_APPEAR = 0
    APPEARING = 1
    VISIBLE = 2
    WILL_DISAPPEAR = 3
    DISAPPEARING = 4
    INVISIBLE = 5


class TransitionState(enum.IntEnum):
    """
    Composite state combining current scene, transition type, and target scene.
    """
    HOLD = 0
    WILL_TRANSITION = 1
    TRANSITIONING = 2


@dataclass(frozen=True)
class State:
    """
    Encapsulates the entire state.
    """
    scene: str
    state: Optional[TransitionState] = None
    prev_scene: Optional[str] = None
    target_scene: Optional[str] = None
    
    def __post_init__(self):
        # note: we circumvent the frozen=True restriction by using `__setattr__`
        if self.prev_scene is None:
            object.__setattr__(self, 'prev_scene', self.scene)
        if self.target_scene is None:
            object.__setattr__(self, 'target_scene', self.scene)

    def __repr__(self):
        if self.state == TransitionState.HOLD:
            state = "HOLD"
            return f"{self.scene}_{state}"
        elif self.state == TransitionState.WILL_TRANSITION:
            state = "WILL_TRANSITION"
        else:
            state = "TRANSITIONING"
        return f"{self.scene}_{state}_TO_{self.target_scene}"


class ControllerExt:
    """
    ControllerExt.
    """
    def __init__(self, ownerComp, initial_scene: str, allowed_transitions: Dict[str, List[str]]):
        # The component to which this extension is attached
        self.ownerComp = ownerComp

        self.timer_container = ownerComp.op('timer_container')
        self.timer_scene = ownerComp.op('timer_scene')
          
        self.allowed_transitions = allowed_transitions
        
        # Stored items: persistent data like the game board
        state = State(scene=initial_scene, state=TransitionState.HOLD)
        storedItems = [
            {"name": "State", "default": state, "readOnly": False, "property": True, "dependable": True},
        ]

        restoreAllDefaults = True  # set this to True if you're editing the class and need a hard reset.
        self.stored = StorageManager(self, ownerComp, storedItems,restoreAllDefaults=restoreAllDefaults)

    def ask_appear(self) -> bool:
        # User logic to decide whether to actually appear.
        # Subclasses can implement this.
        return True
        
    def AskAppear(self) -> bool:
        # Subclasses shouldn't need to modify this.
        if self.timer_container.segment == ContainerState.INVISIBLE and self.ask_appear():
            self.timer_container.par.start.pulse()  # implicitly go to segment 0
            return True
        return False
            
    def ask_disappear(self) -> bool:
        # User logic to decide whether to actually disappear.
        # Subclasses can implement this.
        return True
        
    def AskDisappear(self) -> bool:
        # Subclasses shouldn't need to modify this.
        if self.timer_container.segment == ContainerState.VISIBLE and self.ask_disappear():
            self.timer_container.goTo(segment=ContainerState.WILL_DISAPPEAR)
            return True
        return False
        
    def will_appear_start(self):
        pass
        
    def will_appear_done(self):
        pass
        
    def appearing_start(self):
        pass
        
    def appearing_done(self):
        pass
        
    def visible_start(self):
        pass
        
    def will_disappear_start(self):
        pass
        
    def will_disappear_done(self):
        pass
        
    def disappearing_start(self):
        pass
        
    def disappearing_done(self):
        pass
        
    def invisible_start(self):
        pass
        
    # Methods below are for scenes, not ContainerState.
    
    def allow_transition(self, from_scene: str, to_scene: str):
        """
        A subclass may choose to implement this differently.
        """
        return self.State.state == TransitionState.HOLD
         
    def Transition(self, to_scene: str, instant=False, force=False) -> bool:
        """
        Ask to initiate a transition between two scenes.
        Subclasses shouldn't need to modify this.
        
        Args:
            instant: bool. If True, skip the WILL_TRANSITION and TRANSITIONING. Go straight to HOLD.
        """
        from_scene = self.State.scene
        if force or (self.allow_transition(from_scene, to_scene) and to_scene in self.allowed_transitions.get(from_scene, [])):
            if instant:
                self.State = replace(self.State, scene=to_scene, state=TransitionState.HOLD)
                self.timer_scene.goTo(segment=TransitionState.HOLD)  
            else:
                self.State = replace(self.State, state=TransitionState.WILL_TRANSITION, target_scene=to_scene)
                self.timer_scene.goTo(segment=TransitionState.WILL_TRANSITION)
            return True
        else:
            return False
            
    def hold_start(self):
        pass

    def _hold_start(self):
        """
        Called when entering HOLD state.
        Subclasses should implement hold_start instead of modifying this.
        """
        self.State = replace(self.State, state=TransitionState.HOLD)
        self.hold_start()
        
    def will_transition_start(self):
    	pass

    def _will_transition_start(self):
        """
        Called when entering WILL_TRANSITION state.
        Subclasses should implement will_transition_start instead of modifying this.
        """
        self.will_transition_start()
        
    def will_transition_done(self):
        pass

    def _will_transition_done(self):
        """
        Called when exiting WILL_TRANSITION state.
        Subclasses should implement will_transition_done instead of modifying this.
        """
        self.State = replace(self.State, state=TransitionState.TRANSITIONING, target_scene=self.State.target_scene)
        self.timer_scene.goTo(segment=TransitionState.TRANSITIONING)
        self.will_transition_done()
        
    def transitioning_start(self):
        pass

    def _transitioning_start(self):
        """
        Called when entering TRANSITIONING state.
        Subclasses should implement transitioning_start instead of modifying this.
        """
        self.transitioning_start()
        
    def transitioning_done(self):
    	pass

    def _transitioning_done(self):
        """
        Called when exiting TRANSITIONING state.
        Subclasses should implement transitioning_done instead of modifying this.
        """
        self.State = replace(self.State, prev_scene=self.State.scene, scene=self.State.target_scene, state=TransitionState.HOLD)
        self.timer_scene.goTo(segment=TransitionState.HOLD)
        self.transitioning_done()
        
    def while_transition_active(self, fraction: float):
    	pass

    def _while_transition_active(self, fraction):
        """
        Called continuously during the transition process.
        Subclasses should implement while_transition_active instead of modifying this.
        """
        self.while_transition_active(fraction)
        
    def while_hold(self):
        pass
    
    def _while_hold(self):
        """
        Called when in HOLD state.
        Subclasses should implement while_hold instead of modifying this.
        """
        self.while_hold()

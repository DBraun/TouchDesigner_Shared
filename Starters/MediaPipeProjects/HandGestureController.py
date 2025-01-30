# Author: David Braun https://github.com/DBraun

"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

from TDStoreTools import StorageManager
import TDFunctions as TDF

from state_ext import ControllerExt, TransitionState


class MyControllerExt(ControllerExt):
    def __init__(self, ownerComp):

        initial_scene = "A"
        allowed_transitions = {"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]}

        super().__init__(ownerComp, initial_scene, allowed_transitions)

    def button_hide_clicked(self):
        self.AskDisappear()

    def disappearing_done(self):
        pass

    def invisible_start(self):
        # Ensure we're in state A when we appear next.
        if self.State.scene != "A":
            self.Transition("A", instant=True, force=True)
        op("scenes/gesture_state_A").par.Reset.pulse()

    def hold_start(self):
        print(f"Holding in scene: {self.State.scene}")

    def will_transition_start(self):
        print(
            f"Preparing to transition from {self.State.scene} to {self.State.target_scene}."
        )

    def transitioning_start(self):
        print(f"Transitioning from {self.State.scene} to {self.State.target_scene}.")
        op(f"scenes/gesture_state_{self.State.target_scene}").par.Reset.pulse()

    def transitioning_done(self):
        print(f"Transitioned from {self.State.prev_scene} to {self.State.scene}.")

    def while_transition_active(self, fraction: float):
        print(f"Transition progress: {fraction * 100:.2f}%")

    def while_hold(self):
        pass
        # Logic to automatically bounce between B and C every 5 seconds.
        # if self.State.scene in ["B", "C"] and self.State.state == TransitionState.HOLD:
        # if self.timer_scene["cycles"] > project.cookRate*5:
        # self.Transition("B" if self.State.scene == "C" else "C")

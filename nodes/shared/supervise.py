from .base import BaseSharedManager
from config import SharedKeys, SystemConfig


class SuperviseSharedManager(BaseSharedManager):
    @staticmethod
    def check_max_iterations_reached(shared, function_name):
        """Check if any suite has reached max iterations"""
        max_iterations = BaseSharedManager.get_value(
            shared,
            [SharedKeys.MAX_SUGGESTION_ITERATION],
            SystemConfig.MAX_SUGGESTION_ITERATION,
        )

        return (
            BaseSharedManager.get_value(
                shared, [SharedKeys.SUGGESTION_ITERATION_COUNT, function_name], 0
            )
            >= max_iterations
        )
    
    @staticmethod
    def get_max_suggestion_iteration(shared):
        return BaseSharedManager.get_value(
            shared,
            [SharedKeys.MAX_SUGGESTION_ITERATION],
            SystemConfig.MAX_SUGGESTION_ITERATION,
        )

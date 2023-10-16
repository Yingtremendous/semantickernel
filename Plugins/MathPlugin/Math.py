# !!!!   all native functions must be defined as public methods of a
# class that represents your pulugin

import math
from turtle import st
from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter
from semantic_kernel.orchestration.sk_context import SKContext
class Math:
    # have a class represent the plugin
    # need a function sqrt

    # make sure the sk knwo this is a native function
    # use !!!!! SKFunction decorator above the new method
    # it will automatically register it with kernel when the plugin is loaded 
    @sk_function(
        description="akes the square root of a number", # for planner to automatically create a plan 
        name="Sqrt",
        input_description="The number to take the square root of",
    )
    def square_root(self,number:str) -> str:
        return str(math.sqrt(float(number)))
        # kernel passes lal parameters as strings so they can work seamlessly with semantic functions

    @sk_function(
        description="Multiplies two numbers together",
        name="Multiply",
    )
    @sk_function_context_parameter(
        name="input",
        description="The first number to multiply",
    )
    @sk_function_context_parameter(
        name="number2",
        description="The second number to multiply",
    )
    def add(self, context: SKContext) -> str:
        return str(float(context["input"]) * float(context["number2"]))
# kernel passes lal parameters as strings so they can work seamlessly with semantic functions
        
from django.shortcuts import render
from django.http import HttpResponse
from recursiveapp.models import recursiveFunctions, mathFunctions

def index(request):
    functions_count = recursiveFunctions.objects.all().count()
    calculated_value = ""

    if request.method == "POST":
        posted_text = request.POST['text']
        words = posted_text.split()

        rel_function = 0
        current_function = "addition"
        result = 0

        for word in words:
            if (word.isdigit()):
                result = do_math(current_function, result, int(word))
                calculated_value = int(result)
            elif(word == "+"):
                current_function = "addition"
            elif(word == "*"):
                current_function = "multiplication"
            elif(word == "-"):
                current_function = "subtraction"
            elif(word == "/"):
                current_function = "division"
            else:
                is_registered = recursiveFunctions.objects.filter(name=word)
                if not is_registered:
                    calculated_value = "Some functions in your equation are imaginary."
                    break
                else:
                    rel_function = recursiveFunctions.objects.get(name=word)
                    result = do_math(current_function, result, registered_function(rel_function))
                    calculated_value = int(result)

    context = {
        'functions_count': functions_count,
        'calculated_value': calculated_value
    }
    return render(request, 'index.html', context=context)

def do_math(four_function, field_one, field_two):
    if (four_function == "addition"):
        return (field_one + field_two)
    elif(four_function == "multiplication"):
        return (field_one * field_two)
    elif(four_function == "subtraction"):
        return (field_one - field_two)
    elif(four_function == "division"):
        return (field_one / field_two)

def registered_function(relative_function):
    if (str(relative_function.field_one).isdigit()):
        if (str(relative_function.field_two).isdigit()):
            return do_math(str(relative_function.math_function), int(relative_function.field_one), int(relative_function.field_two))
        else:
            insider_function = recursiveFunctions.objects.get(name=str(relative_function.field_two))
            return do_math(str(relative_function.math_function), int(relative_function.field_one), registered_function(insider_function))
    else:
        if (str(relative_function.field_two).isdigit()):
            insider_function = recursiveFunctions.objects.get(name=str(relative_function.field_one))
            return do_math(str(relative_function.math_function), registered_function(insider_function), int(relative_function.field_two))
        else:
            insider_function = recursiveFunctions.objects.get(name=str(relative_function.field_one))
            insider_function_second = recursiveFunctions.objects.get(name=str(relative_function.field_two))
            return do_math(str(relative_function.math_function), registered_function(insider_function), registered_function(insider_function_second))

        
            
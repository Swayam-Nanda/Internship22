from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect

def add_employee(request):
    if request.method == "POST":
        name = request.POST.get("a1")
        email = request.POST.get("a2")
        contact = request.POST.get("a3")
        gender = request.POST.get("gender")
        password = request.POST.get("a4")

        # Determine role prefix (E, HR, ADM)
        role = "E"  # default role
        if "hr" in email.lower():
            role = "HR"
        elif "admin" in email.lower() or "adm" in email.lower():
            role = "ADM"

        prefix = f"TD-ERP-{role}"

        # Count current documents of this role type
        existing = db.collection("employees").where("uid", ">=", prefix).where("uid", "<", prefix + "~").stream()
        count = sum(1 for _ in existing) + 1  # +1 for the new one

        uid_number = str(count).zfill(5)
        full_uid = f"{prefix}-{uid_number}"

        data = {
            "uid": full_uid,
            "name": name,
            "email": email,
            "contact": contact,
            "gender": gender,
            "password": password,
            "role": role
        }

        db.collection("employees").add(data)
        request.session['employee_success'] = f"Employee added with UID {full_uid}"
        
        return redirect("/add-employee/")  # <— 👈 Redirect here!

    message = request.session.pop('employee_success', None)  # Get and remove message
    return render(request, "add_employee.html", {"message": message})


def get_employees(request):
    search_query = request.GET.get('search', '').strip().lower()

    # Fetch all employees
    employees_ref = db.collection("employees").stream()

    employees = []
    for emp in employees_ref:
        data = emp.to_dict()
        if search_query:
            # Check if query matches any field
            if (
                search_query in data.get("name", "").lower()
                or search_query in data.get("uid", "").lower()
                or search_query in data.get("email", "").lower()
                or search_query in data.get("contact", "").lower()
            ):
                employees.append(data)
        else:
            employees.append(data)

    return render(request, "get_employees.html", {"employees": employees, "search_query": search_query})


def signin(request):
    return render(request, 'signin.html')


# Create your views here.

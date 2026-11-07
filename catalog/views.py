
from django.shortcuts import render
from django.http import Http404

COURSES_DATA = [
    {
        'id': 101,
        'code': 'DTI412',
        'title': 'Special Topic in Application Development',
        'description': 'Learn application development using modern technologies.',
        'credits': 3,
        'instructor': 'Course Instructor',
    },
    {
        'id': 102,
        'code': 'DTI201',
        'title': 'Database Systems & Data Modeling',
        'description': 'Learn database design and data modeling.',
        'credits': 3,
        'instructor': 'Course Instructor',
    },
    {
        'id': 103,
        'code': 'DTI305',
        'title': 'Frontend Web Technologies & React',
        'description': 'Learn frontend web development and React.',
        'credits': 3,
        'instructor': 'Course Instructor',
    },
]


def home_view(request):
    context = {
        'total_courses': len(COURSES_DATA),
        'featured_course': COURSES_DATA[0],
    }
    return render(request, 'catalog/home.html', context)


def course_list_view(request):
    search_query = request.GET.get('q', '').strip()

    filtered_courses = [
        course for course in COURSES_DATA
        if search_query.lower() in course['title'].lower()
        or search_query.lower() in course['code'].lower()
    ]

    context = {
        'courses': filtered_courses,
        'search_query': search_query,
    }

    return render(request, 'catalog/course_list.html', context)


def course_detail_view(request, course_id):
    course = next(
        (course for course in COURSES_DATA if course['id'] == course_id),
        None
    )

    if course is None:
        raise Http404("Course not found")

    return render(request, 'catalog/course_detail.html', {'course': course})


def inquiry_view(request):
    errors = {}
    submitted_data = {}

    if request.method == 'POST':
        student_name = request.POST.get('student_name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        submitted_data = {
            'student_name': student_name,
            'email': email,
            'message': message,
        }

        if not student_name:
            errors['student_name'] = 'Name is required.'

        if not email:
            errors['email'] = 'Email is required.'

        if not message:
            errors['message'] = 'Message is required.'

        if not errors:
            return render(request, 'catalog/inquiry.html', {
                'submitted': True,
                'courses': COURSES_DATA,
            })

    return render(request, 'catalog/inquiry.html', {
        'courses': COURSES_DATA,
        'errors': errors,
        'submitted_data': submitted_data,
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q, Sum

# Import models
from video_courses.models import Category
from testseries.models import TestSeries, Test, Question, Subject, marks_num


@login_required
@user_passes_test(lambda user: user.is_superuser or user.is_staff)
def test_series_delete(request, pk):
    """Delete a test series"""
    series = get_object_or_404(TestSeries, pk=pk)
    if request.method == 'POST':
        title = series.title
        series.delete()
        messages.success(request, f'Test series "{title}" has been deleted successfully.')
        return redirect('test_series_manage')
    return redirect('test_series_manage')

    
# ---------------------------------------------
# Utility Functions
# ---------------------------------------------
def is_admin(user):
    return user.is_superuser or user.is_staff

# ---------------------------------------------
# Test Series Management Views
# ---------------------------------------------
@login_required
@user_passes_test(is_admin)
def test_series_manage(request):
    """Manage all test series courses"""
    search_query = request.GET.get('search', '')
    test_series = TestSeries.objects.all()

    # Apply filters
    if search_query:
        test_series = test_series.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    test_series = test_series.order_by('-created_at')

    # Pagination
    paginator = Paginator(test_series, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Live stats for the visible page only, counted in the database.
    page_ids = [series.pk for series in page_obj]
    stats = {
        row['pk']: row
        for row in TestSeries.objects.filter(pk__in=page_ids).values('pk').annotate(
            tests_n=Count('tests', distinct=True),
            questions_n=Count('tests__questions'),
            marks_n=Sum('tests__questions__marks'),
        )
    }
    for series in page_obj:
        row = stats.get(series.pk, {})
        series.total_tests = row.get('tests_n', 0)
        series.total_questions = row.get('questions_n', 0)
        series.total_marks = marks_num(row.get('marks_n'))

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'testseries/manage.html', context)

def _board_fields_from_post(post):
    """(board, grade, stream, exam) from the test series form; stream is kept only for Class 11-12."""
    board = post.get('board', '') if post.get('board') in dict(TestSeries.BOARD_CHOICES) else ''
    grade = int(post['grade']) if (post.get('grade') or '').isdigit() and 1 <= int(post['grade']) <= 12 else None
    stream = post.get('stream', '') if grade in (11, 12) and post.get('stream') in dict(TestSeries.STREAM_CHOICES) else ''
    exam = (post.get('exam') or '').strip()[:100]
    return board, grade, stream, exam


def _board_choice_context():
    return {
        'board_choices': TestSeries.BOARD_CHOICES,
        'grade_choices': TestSeries.GRADE_CHOICES,
        'stream_choices': TestSeries.STREAM_CHOICES,
        'exam_choices': list(Category.objects.order_by('name').values_list('name', flat=True)),
    }

# ---------------------------------------------
# Create Test Series Course
# ---------------------------------------------
@login_required
@user_passes_test(is_admin)
def test_series_create(request):
    """Create new test series course"""
    if request.method == 'POST':
        title = request.POST.get('title')
        board, grade, stream, exam = _board_fields_from_post(request.POST)
        description = request.POST.get('description')
        difficulty = request.POST.get('difficulty')
        estimated_duration = request.POST.get('estimated_duration')
        is_free = request.POST.get('is_free') == 'on'
        price = request.POST.get('price', 0)
        has_negative_marking = request.POST.get('has_negative_marking') == 'on'
        negative_marks = request.POST.get('negative_marks', 0.25)
        pass_percentage = request.POST.get('pass_percentage', 40)
        is_featured = request.POST.get('is_featured') == 'on'
        thumbnail = request.FILES.get('thumbnail')

        try:
            test_series = TestSeries.objects.create(
                title=title,
                board=board,
                grade=grade,
                stream=stream,
                exam=exam,
                description=description,
                difficulty=difficulty,
                estimated_duration=estimated_duration,
                is_free=is_free,
                price=price if not is_free else 0,
                has_negative_marking=has_negative_marking,
                negative_marks=negative_marks,
                pass_percentage=pass_percentage,
                is_featured=is_featured,
                thumbnail=thumbnail,
            )
            messages.success(request, f'Test series course "{title}" created successfully! You can now schedule tests under it.')
            return redirect('test_series_detail', pk=test_series.pk)

        except Exception as e:
            messages.error(request, f'Error creating test series course: {str(e)}')

    return render(request, 'testseries/create.html', _board_choice_context())



# ---------------------------------------------
# Test Series Detail - View All Scheduled Tests
# ---------------------------------------------
@login_required
@user_passes_test(is_admin)
def test_series_detail(request, pk):
    """View all scheduled tests in a series"""
    test_series = get_object_or_404(TestSeries, pk=pk)
    tests = test_series.tests.prefetch_related('questions').order_by('created_at')

    for test in tests:
        test.question_count = test.questions.count()
        test.total_marks = marks_num(sum(q.marks for q in test.questions.all()))
        test.difficulty_breakdown = {
            'easy': test.questions.filter(difficulty='easy').count(),
            'medium': test.questions.filter(difficulty='medium').count(),
            'hard': test.questions.filter(difficulty='hard').count(),
        }

    context = {
        'test_series': test_series,
        'tests': tests,
        'total_questions': sum(test.question_count for test in tests),
        'total_marks': sum(test.total_marks for test in tests),
    }
    return render(request, 'testseries/detail.html', context)

# ---------------------------------------------
# Edit Test Series Course
# ---------------------------------------------
@login_required
@user_passes_test(is_admin)
def test_series_edit(request, pk):
    """Edit test series course"""
    test_series = get_object_or_404(TestSeries, pk=pk)

    if request.method == 'POST':
        old_title = test_series.title
        test_series.title = request.POST.get('title')
        test_series.board, test_series.grade, test_series.stream, test_series.exam = _board_fields_from_post(request.POST)
        test_series.description = request.POST.get('description')
        test_series.difficulty = request.POST.get('difficulty')
        test_series.estimated_duration = request.POST.get('estimated_duration')
        test_series.is_free = request.POST.get('is_free') == 'on'
        test_series.price = request.POST.get('price', 0) if not test_series.is_free else 0
        test_series.has_negative_marking = request.POST.get('has_negative_marking') == 'on'
        test_series.negative_marks = request.POST.get('negative_marks', 0.25)
        test_series.pass_percentage = request.POST.get('pass_percentage', 40)
        test_series.is_featured = request.POST.get('is_featured') == 'on'
        test_series.is_active = request.POST.get('is_active') == 'on'

        if request.FILES.get('thumbnail'):
            test_series.thumbnail = request.FILES.get('thumbnail')

        try:
            test_series.save()
            messages.success(request, f'Test series course "{old_title}" updated successfully!')
            return redirect('test_series_detail', pk=test_series.pk)
        except Exception as e:
            messages.error(request, f'Error updating test series course: {str(e)}')

    return render(request, 'testseries/edit.html', {
        'test_series': test_series,
        **_board_choice_context(),
    })

def _calculator_from_post(post):
    value = post.get('calculator', 'none')
    return value if value in dict(Test.CALCULATOR_CHOICES) else 'none'


def _paper_fields_from_post(post):
    """(paper_type, exam_year) from the test form; the year only applies to previous year papers."""
    paper_type = post.get('paper_type', 'mock')
    if paper_type not in dict(Test.PAPER_TYPES):
        paper_type = 'mock'
    year = post.get('exam_year', '').strip()
    exam_year = int(year) if paper_type == 'pyp' and year.isdigit() and 1950 <= int(year) <= 2100 else None
    return paper_type, exam_year


# ---------------------------------------------
# Create Scheduled Test
# ---------------------------------------------
@login_required
@user_passes_test(is_admin)
def test_create(request, series_pk):
    """Schedule a new test for a series"""
    test_series = get_object_or_404(TestSeries, pk=series_pk)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        duration_minutes = request.POST.get('duration_minutes')
        max_attempts = request.POST.get('max_attempts', 1)
        shuffle_questions = request.POST.get('shuffle_questions') == 'on'
        show_result_immediately = request.POST.get('show_result_immediately') == 'on'
        allow_review = request.POST.get('allow_review') == 'on'
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        paper_type, exam_year = _paper_fields_from_post(request.POST)

        try:
            test = Test.objects.create(
                test_series=test_series,
                title=title,
                description=description,
                duration_minutes=duration_minutes,
                max_attempts=max_attempts,
                shuffle_questions=shuffle_questions,
                show_result_immediately=show_result_immediately,
                allow_review=allow_review,
                calculator=_calculator_from_post(request.POST),
                is_demo=request.POST.get('is_demo') == 'on',
                paper_type=paper_type,
                exam_year=exam_year,
                start_time=start_time if start_time else None,
                end_time=end_time if end_time else None,
            )
            messages.success(
                request,
                f'Scheduled test "{title}" created successfully under "{test_series.title}"! Now add questions to complete the test.'
            )
            return redirect('test_edit', pk=test.pk)

        except Exception as e:
            messages.error(request, f'Error creating scheduled test: {str(e)}')

    return render(request, 'testseries/test_create.html', {'test_series': test_series})

# ---------------------------------------------
# Edit Scheduled Test
# ---------------------------------------------
@login_required
@user_passes_test(is_admin)
def test_edit(request, pk):
    """Edit scheduled test and manage questions"""
    test = get_object_or_404(Test, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_test':
            old_title = test.title
            test.title = request.POST.get('title')
            test.description = request.POST.get('description')
            test.duration_minutes = request.POST.get('duration_minutes')
            test.max_attempts = request.POST.get('max_attempts')
            test.shuffle_questions = request.POST.get('shuffle_questions') == 'on'
            test.show_result_immediately = request.POST.get('show_result_immediately') == 'on'
            test.allow_review = request.POST.get('allow_review') == 'on'
            test.calculator = _calculator_from_post(request.POST)
            test.is_demo = request.POST.get('is_demo') == 'on'
            test.paper_type, test.exam_year = _paper_fields_from_post(request.POST)
            test.is_active = request.POST.get('is_active') == 'on'

            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            test.start_time = start_time if start_time else None
            test.end_time = end_time if end_time else None

            try:
                test.save()
                messages.success(request, f'Scheduled test "{old_title}" updated successfully!')
            except Exception as e:
                messages.error(request, f'Error updating scheduled test: {str(e)}')

    questions = test.questions.select_related('subject').order_by('order')
    subjects = Subject.objects.filter(is_active=True)

    # Test statistics
    test.question_count = questions.count()
    test.total_marks = sum(q.marks for q in questions)
    test.difficulty_stats = {
        'easy': questions.filter(difficulty='easy').count(),
        'medium': questions.filter(difficulty='medium').count(),
        'hard': questions.filter(difficulty='hard').count(),
    }

    # Subject-wise breakdown
    test.subject_stats = {}
    for question in questions:
        subject = question.subject.name if question.subject else 'General'
        test.subject_stats[subject] = test.subject_stats.get(subject, 0) + 1

    context = {
        'test': test,
        'questions': questions,
        'subjects': subjects,
    }
    return render(request, 'testseries/test_edit.html', context)

# ---------------------------------------------
# Create Question
# ---------------------------------------------
@login_required
@user_passes_test(is_admin)
def question_create(request, test_pk):
    """Create new question for a scheduled test"""
    test = get_object_or_404(Test, pk=test_pk)

    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        question_type = request.POST.get('question_type')
        difficulty = request.POST.get('difficulty')
        marks = request.POST.get('marks', 1)
        negative_marks = request.POST.get('negative_marks', 0.25)
        subject_id = request.POST.get('subject')
        explanation = request.POST.get('explanation', '')
        question_image = request.FILES.get('question_image')
        solution_image = request.FILES.get('solution_image')

        # Determine order
        last_question = test.questions.order_by('-order').first()
        order = (last_question.order + 1) if last_question else 1

        # Prepare options and answers
        options = {}
        correct_answer = {}

        if question_type in ['mcq_single', 'mcq_multiple']:
            for i in range(1, 5):  # 4 options (a–d)
                option_text = request.POST.get(f'option_{i}')
                if option_text:
                    options[chr(96 + i)] = option_text  # a, b, c, d

            if question_type == 'mcq_single':
                correct_answer = request.POST.get('correct_answer')
            else:
                correct_answer = request.POST.getlist('correct_answers')

        elif question_type == 'true_false':
            options = {'a': 'True', 'b': 'False'}
            correct_answer = request.POST.get('correct_answer')

        elif question_type in ['fill_blank', 'numerical']:
            correct_answer = request.POST.get('correct_answer')

        try:
            subject = Subject.objects.get(id=subject_id) if subject_id else None
            Question.objects.create(
                test=test,
                subject=subject,
                question_type=question_type,
                difficulty=difficulty,
                question_text=question_text,
                question_image=question_image,
                marks=marks,
                negative_marks=negative_marks,
                options=options,
                correct_answer=correct_answer,
                explanation=explanation,
                solution_image=solution_image,
                order=order,
            )
            messages.success(
                request,
                f'✅ Question #{order} added successfully to "{test.title}"! Test now has {test.questions.count()} questions.'
            )
            return redirect('test_edit', pk=test.pk)

        except Exception as e:
            messages.error(request, f'Error creating question: {str(e)}')

    subjects = Subject.objects.filter(is_active=True)
    return render(request, 'testseries/question_create.html', {'test': test, 'subjects': subjects})

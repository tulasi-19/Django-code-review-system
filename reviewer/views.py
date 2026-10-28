from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegisterForm, CodeSubmissionForm
from .models import CodeSubmission, Review
from .review_engine import generate_review


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully. Welcome!")
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "reviewer/register.html", {"form": form})


@login_required
def dashboard_view(request):
    submissions = CodeSubmission.objects.filter(user=request.user)[:5]
    total = CodeSubmission.objects.filter(user=request.user).count()
    reviewed = CodeSubmission.objects.filter(user=request.user, status="reviewed").count()
    avg_score = 0
    reviews = Review.objects.filter(submission__user=request.user)
    if reviews.exists():
        avg_score = round(sum(r.score for r in reviews) / reviews.count())
    context = {
        "submissions": submissions,
        "total": total,
        "reviewed": reviewed,
        "avg_score": avg_score,
    }
    return render(request, "reviewer/dashboard.html", context)


@login_required
def submit_code_view(request):
    if request.method == "POST":
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.save()

            try:
                result = generate_review(submission.code, submission.language)
                Review.objects.create(
                    submission=submission,
                    feedback=result["feedback"],
                    score=result["score"],
                    issues_found=result["issues_found"],
                    engine_used=result["engine"],
                )
                submission.status = "reviewed"
            except Exception:
                submission.status = "failed"
                messages.error(request, "Review generation failed. Please try again.")
            submission.save()

            return redirect("review_detail", pk=submission.pk)
    else:
        form = CodeSubmissionForm()
    return render(request, "reviewer/submit_code.html", {"form": form})


@login_required
def review_detail_view(request, pk):
    submission = get_object_or_404(CodeSubmission, pk=pk, user=request.user)
    review = getattr(submission, "review", None)
    return render(request, "reviewer/review_detail.html", {"submission": submission, "review": review})


@login_required
def review_history_view(request):
    submissions = CodeSubmission.objects.filter(user=request.user)
    return render(request, "reviewer/review_history.html", {"submissions": submissions})

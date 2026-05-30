from celery import shared_task
from datetime import date, timedelta


@shared_task
def test_task():
    print("Test task worked!")
    return "ok"


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3
)
def send_assignment_notification(user_id, task_title):
    from apps.core.models import Notification
    from django.contrib.auth import get_user_model
    User = get_user_model()

    user = User.objects.get(id=user_id)
    Notification.objects.create(
        user=user,
        title="Task assigned to you",
        message=f'"{task_title}" task assigned to you.'
    )
    print(f"Notification created for {user.email}")


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3
)
def send_deadline_email(email, task_title, due_date):
    from django.core.mail import send_mail

    send_mail(
        subject=f'Deadline Reminder: {task_title}',
        message=f'"{task_title}" task deadline is tomorrow ({due_date})!',
        from_email='noreply@teamflow.com',
        recipient_list=[email],
        fail_silently=False,
    )
    print(f"Email sent to {email} for task: {task_title}")
    return f"Email sent to {email}"


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3
)
def send_deadline_reminders():
    from apps.tasks.models import Task
    from apps.core.models import Notification

    tomorrow = date.today() + timedelta(days=1)

    tasks = Task.objects.filter(
        due_date=tomorrow,
        assignee__isnull=False
    ).select_related('assignee')

    for task in tasks:
        Notification.objects.create(
            user=task.assignee,
            title="Task deadline tomorrow",
            message=f'"{task.title}" task deadline is tomorrow ({task.due_date})!'
        )
        send_deadline_email.delay(
            task.assignee.email,
            task.title,
            str(task.due_date)
        )

    print(f"{tasks.count()} deadline reminder sent.")
    return tasks.count()
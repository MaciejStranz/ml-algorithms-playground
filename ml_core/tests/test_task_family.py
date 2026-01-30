import pytest

from ml_core.common.types import TaskType, TaskFamily, task_family_from_task


def test_task_family_mapping_basic():
    assert task_family_from_task(TaskType.BINARY) == TaskFamily.CLASSIFICATION
    assert task_family_from_task(TaskType.MULTICLASS) == TaskFamily.CLASSIFICATION
    assert task_family_from_task(TaskType.REGRESSION) == TaskFamily.REGRESSION

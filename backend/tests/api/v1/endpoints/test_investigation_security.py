from fastapi.params import Depends

from app.api.v1.endpoints.investigation import investigate_terraform


def test_investigation_endpoint_requires_rbac_dependency():
    dependencies = [
        default
        for default in (investigate_terraform.__defaults__ or ())
        if isinstance(default, Depends)
    ]

    rbac_dependencies = [
        dependency
        for dependency in dependencies
        if getattr(dependency.dependency, "__module__", "")
        == "app.api.v1.dependencies.rbac"
    ]

    assert len(rbac_dependencies) == 1

    dependency = rbac_dependencies[0].dependency

    assert dependency.__name__ == "dependency"

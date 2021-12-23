"""Field definitions."""

from dataclasses import field as _field, Field


__all__ = ['field']


def make_field(*args, **kwargs) -> Field:
    """Delegates to dataclasses.field() while
    passing excess kwargs as metadata.
    """

    metadata_override = kwargs.pop('metadata', {})
    metadata = {
        key: value for key, value in kwargs.items()
        if key not in _field.__code__.co_varnames
    }
    metadata.update(metadata_override)
    return _field(*args, metadata=metadata, **kwargs)


def field(*args, index: bool = False, primary: bool = False,
          unique: bool = False, **kwargs) -> Field:
    """Creates a field."""
    return make_field(*args, index=index, primary=primary, unique=unique,
                      **kwargs)

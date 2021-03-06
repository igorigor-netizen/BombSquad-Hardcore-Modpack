from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Dict, \
        Any

from ba import Activity, Node, GameActivity
from _ba import get_foreground_host_activity
from ..enums import Actions, ActivityAttrs

import weakref


def getactivity(gameactivity: bool = False) -> Optional[Activity]:
    activity = get_foreground_host_activity()
    if activity:
        if (gameactivity and
                isinstance(activity.__class__, GameActivity) and
                not getattr(activity, 'has_ended', lambda: True)()) or not gameactivity:
            return weakref.ref(activity)()
    return None


def activityglobals(
        activity: Optional[Activity] = None) -> Optional[Node]:
    if not activity:
        activity = getactivity()
    return getattr(activity, '_globalsnode', None)


def action(
        _action: Actions = Actions.GET,
        obj: Optional[Dict[str, Any]] = None) -> Any:
    if not obj:
        return
    elif _action not in Actions:
        raise ValueError('Invalid action:', _action)
    elif 'type' not in obj:
        raise ValueError('Invalid obj, key "type" is needed')
    g = activityglobals(None)
    if _action == Actions.GET:
        if obj['type'] == 'tint':
            return getattr(g,
                           ActivityAttrs.TINT.value, g.tint)
        elif obj['type'] == 'motion':
            return getattr(g,
                           ActivityAttrs.MOTION.value, g.slow_motion)
        else:
            raise ValueError('Invalid type:', obj['type'])
    elif _action == Actions.SET:
        if 'value' not in obj:
            raise ValueError('Invalid obj, key "value" is needed')
        val = obj['value']
        if obj['type'] == 'tint':
            if not isinstance(val, tuple) or len(val) != 3:
                raise ValueError('only 3-len tuple')
            g.tint = val
            setattr(g,
                    ActivityAttrs.TINT.value, val)
        elif obj['type'] == 'motion':
            if not isinstance(val, bool):
                raise ValueError('only booled')
            g.slow_motion = val
            setattr(g,
                    ActivityAttrs.MOTION.value, val)
        else:
            raise ValueError('Invalid type:', obj['type'])

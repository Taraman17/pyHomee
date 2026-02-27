"""Data model for homeegrams (automations) in Homee."""

from datetime import datetime, timezone
from urllib.parse import unquote
from typing import Any

from pyHomee.model import HomeeObject


class HomeegramTcaItem:
    # TCA stands for trigger, condition, action. This class is used as a base class for these.
    """Representation of a homeegram trigger."""

    def __init__(self, tca_dict: dict[str, Any]) -> None:
        """Initialize a tcaItem."""
        self._data = tca_dict

    @property
    def data(self) -> dict[str, Any]:
        """Return the raw tcaItem dict."""
        return dict(self._data)

    @property
    def id(self) -> int:
        """Id of the tcaItem, unique in Homee."""
        return int(self._data["id"])

    @property
    def homeegram_id(self) -> int:
        """Id of the homeegram the tcaItem belongs to."""
        return int(self._data["homeegram_id"])


class HomeegramTriggers:
    """Representation of homeegram triggers."""

    class HomeegramTimeTrigger(HomeegramTcaItem):
        """Representation of a homeegram time trigger."""

        @property
        def dtstart(self) -> datetime:
            """Start date/time of the time trigger."""
            return datetime.strptime(self._data["dtstart"], "%Y%m%dT%H%M%SZ").replace(
                tzinfo=timezone.utc
            )

        @property
        def rrule(self) -> str:
            """Recurrence rule of the time trigger."""
            return str(self._data["rrule"])

        @property
        def next_invoaction(self) -> datetime | None:
            """Time of the next invocation of the time trigger."""
            if "next_invocation" in self._data:
                return datetime.strptime(
                    self._data["next_invocation"], "%Y-%m-%dT%H:%M:%S"
                )
            else:
                return None

    class HomeegramAttributeTrigger(HomeegramTcaItem):
        """Representation of a homeegram attribute trigger."""

        @property
        def node_id(self) -> int:
            """Id of the node the triggering attribute belongs to."""
            return int(self._data["node_id"])

        @property
        def attribute_id(self) -> int:
            """Id of the triggering attribute."""
            return int(self._data["attribute_id"])

        @property
        def operator(self) -> int:
            """Operator used in the trigger."""
            return int(self._data["operator"])

        @property
        def operand(self) -> int:
            """Operand used in the trigger."""
            return int(self._data["operand"])

        @property
        def value(self) -> float:
            """Value of the trigger."""
            return float(self._data["value"])

    class HomeegramWebhookTrigger(HomeegramTcaItem):
        """Representation of a homeegram webhook trigger."""

        @property
        def event(self) -> str:
            """Event name of the webhook trigger."""
            return str(self._data["event"])

    class HomeegramCelestialTrigger(HomeegramTcaItem):
        """Representation of a homeegram celestial trigger."""

        @property
        def celestial_type(self) -> int:
            """Type of celestial event triggering this trigger."""
            return int(self._data["celestial_type"])

        @property
        def time_offset(self) -> int:
            """Time offset in minutes for the celestial trigger."""
            return int(self._data["time_offset"])

    class HomeegramGroupTrigger(HomeegramTcaItem):
        """Representation of a homeegram group trigger."""

        @property
        def group_id(self) -> int:
            """Id of the group triggering this trigger."""
            return int(self._data["group_id"])

        @property
        def attribute_type(self) -> int:
            """Attribute type of the group trigger."""
            return int(self._data["attribute_type"])

        @property
        def operator(self) -> int:
            """Operator used in the trigger."""
            return int(self._data["operator"])

        @property
        def value(self) -> float:
            """Value of the trigger."""
            return float(self._data["value"])

    class HomeegramUserTrigger(HomeegramTcaItem):
        """Representation of a homeegram user trigger."""

        @property
        def user_id(self) -> int:
            """Id of the user triggering this trigger."""
            return int(self._data["user_id"])

        @property
        def value(self) -> int:
            """Value of the user trigger."""
            return int(self._data["value"])

        @property
        def data(self) -> dict[str, list]:
            """Return the raw triggers dict."""
            return dict(self._data)

    def __init__(self, triggers: dict[str, list[dict[str, Any]]]) -> None:
        """Initialize triggers."""
        self._data = triggers

    @property
    def data(self) -> dict[str, list[dict[str, Any]]]:
        """Return the raw triggers dict."""
        return dict(self._data)

    @property
    # A switch trigger has no additional properties.
    def switch_triggers(self) -> list[HomeegramTcaItem]:
        """Return the list of switch triggers."""
        return [HomeegramTcaItem(trigger) for trigger in self._data["switch_triggers"]]

    @property
    def time_triggers(self) -> list[HomeegramTimeTrigger]:
        """Return the list of time triggers."""
        return [
            self.HomeegramTimeTrigger(trigger)
            for trigger in self._data["time_triggers"]
        ]

    @property
    def attribute_triggers(self) -> list[HomeegramAttributeTrigger]:
        """Return the list of attribute triggers."""
        return [
            self.HomeegramAttributeTrigger(trigger)
            for trigger in self._data["attribute_triggers"]
        ]

    @property
    def webhook_triggers(self) -> list[HomeegramWebhookTrigger]:
        """Return the list of webhook triggers."""
        return [
            self.HomeegramWebhookTrigger(trigger)
            for trigger in self._data["webhook_triggers"]
        ]

    @property
    # For homeegram triggers I have no information about the structure of
    # the trigger dict, so I return a list of basic HomeegramTcaItems.
    def homeegram_triggers(self) -> list[HomeegramTcaItem]:
        """Return the list of homeegram triggers."""
        return [
            HomeegramTcaItem(trigger) for trigger in self._data["homeegram_triggers"]
        ]

    @property
    def celestial_triggers(self) -> list[HomeegramCelestialTrigger]:
        """Return the list of celestial triggers."""
        return [
            self.HomeegramCelestialTrigger(trigger)
            for trigger in self._data["celestial_triggers"]
        ]

    @property
    # For plan triggers I have no information about the structure of
    # the trigger dict, so I return a list of basic HomeegramTcaItems.
    def plan_triggers(self) -> list[HomeegramTcaItem]:
        """Return the list of plan triggers."""
        return [HomeegramTcaItem(trigger) for trigger in self._data["plan_triggers"]]

    @property
    def group_triggers(self) -> list[HomeegramGroupTrigger]:
        """Return the list of group triggers."""
        return [
            self.HomeegramGroupTrigger(trigger)
            for trigger in self._data["group_triggers"]
        ]

    @property
    def user_triggers(self) -> list[HomeegramUserTrigger]:
        """Return the list of user triggers."""
        return [
            self.HomeegramUserTrigger(trigger)
            for trigger in self._data["user_triggers"]
        ]


class HomeegramConditions:
    """Representation of homeegram conditions."""

    class HomeegramCondition(HomeegramTcaItem):
        """Representation of a homeegram condition."""

        @property
        def check_moment(self) -> int:
            """Check moment of the condition."""
            return int(self._data["check_moment"])

    class HomeegramTimeCondition(HomeegramCondition):
        """Representation of a homeegram time condition."""

        @property
        def dtstart(self) -> datetime:
            """Start date/time of the time condition."""
            return datetime.strptime(self._data["dtstart"], "%Y%m%dT%H%M%SZ").replace(
                tzinfo=timezone.utc
            )

        @property
        def rrule(self) -> str:
            """Recurrence rule of the time condition."""
            return str(self._data["rrule"])

        @property
        def duration(self) -> str:
            """Duration of the time condition."""
            return str(self._data["duration"])

    class HomeegramAttributeCondition(HomeegramCondition):
        """Representation of a homeegram attribute condition."""

        @property
        def node_id(self) -> int:
            """Id of the node the condition attribute belongs to."""
            return int(self._data["node_id"])

        @property
        def attribute_id(self) -> int:
            """Id of the condition attribute."""
            return int(self._data["attribute_id"])

        @property
        def operator(self) -> int:
            """Operator used in the condition."""
            return int(self._data["operator"])

        @property
        def operand(self) -> int:
            """Operand used in the condition."""
            return int(self._data["operand"])

        @property
        def value(self) -> float:
            """Value of the condition."""
            return float(self._data["value"])

    class HomeegramHomeegramCondition(HomeegramCondition):
        """Representation of a homeegram homeegram condition."""

        @property
        def source_homeegram_id(self) -> int:
            """Id of the source homeegram for this condition."""
            return int(self._data["source_homeegram_id"])

        @property
        def homeegram_event(self) -> int:
            """Homeegram event type for this condition."""
            return int(self._data["homeegram_event"])

    class HomeegramCelestialCondition(HomeegramCondition):
        """Representation of a homeegram celestial condition."""

        @property
        def time_of_day(self) -> int:
            """Time of day for this celestial condition."""
            return int(self._data["time_of_day"])

    class HomeegramGroupCondition(HomeegramCondition):
        """Representation of a homeegram group condition."""

        @property
        def group_id(self) -> int:
            """Id of the group for this condition."""
            return int(self._data["group_id"])

        @property
        def attribute_type(self) -> int:
            """Attribute type of the group condition."""
            return int(self._data["attribute_type"])

        @property
        def operator(self) -> int:
            """Operator used in the condition."""
            return int(self._data["operator"])

        @property
        def value(self) -> float:
            """Value of the condition."""
            return float(self._data["value"])

        @property
        def scope(self) -> int:
            """Scope of the group condition."""
            return int(self._data["scope"])

    class HomeegramUserCondition(HomeegramCondition):
        """Representation of a homeegram user condition."""

        @property
        def user_id(self) -> int:
            """Id of the user for this condition."""
            return int(self._data["user_id"])

        @property
        def value(self) -> int:
            """Value of the user condition."""
            return int(self._data["value"])

    def __init__(self, conditions: dict[str, Any]) -> None:
        """Initialize conditions."""
        self._data = conditions

    @property
    def data(self) -> dict[str, list]:
        """Return the raw conditions dict."""
        return dict(self._data)

    @property
    def time_conditions(self) -> list[HomeegramTimeCondition]:
        """Return the list of time conditions."""
        return [
            self.HomeegramTimeCondition(condition)
            for condition in self._data["time_conditions"]
        ]

    @property
    def attribute_conditions(self) -> list[HomeegramAttributeCondition]:
        """Return the list of attribute conditions."""
        return [
            self.HomeegramAttributeCondition(condition)
            for condition in self._data["attribute_conditions"]
        ]

    @property
    def homeegram_conditions(self) -> list[HomeegramTcaItem]:
        # For homeegram conditions I have no information about the structure of
        # the condition dict, so I return a list of basic HomeegramTcaItems.
        """Return the list of homeegram conditions."""
        return [
            HomeegramTcaItem(condition)
            for condition in self._data["homeegram_conditions"]
        ]

    @property
    def celestial_conditions(self) -> list[HomeegramCelestialCondition]:
        """Return the list of celestial conditions."""
        return [
            self.HomeegramCelestialCondition(condition)
            for condition in self._data["celestial_conditions"]
        ]

    @property
    def plan_conditions(self) -> list[HomeegramTcaItem]:
        # For plan conditions I have no information about the structure of
        # the condition dict, so I return a list of basic HomeegramTcaItems.
        """Return the list of plan conditions."""
        return [
            HomeegramTcaItem(condition) for condition in self._data["plan_conditions"]
        ]

    @property
    def group_conditions(self) -> list[HomeegramGroupCondition]:
        """Return the list of group conditions."""
        return [
            self.HomeegramGroupCondition(condition)
            for condition in self._data["group_conditions"]
        ]

    @property
    def user_conditions(self) -> list[HomeegramUserCondition]:
        """Return the list of user conditions."""
        return [
            self.HomeegramUserCondition(condition)
            for condition in self._data["user_conditions"]
        ]


class HomeegramActions:
    """Representation of homeegram actions."""

    class HomeegramAction(HomeegramTcaItem):
        """Representation of a homeegram action."""

        @property
        def delay(self) -> int:
            """Delay in seconds before the action is executed."""
            return int(self._data["delay"])

    class HomeegramAttributeAction(HomeegramAction):
        """Representation of a homeegram attribute action."""

        @property
        def node_id(self) -> int:
            """Id of the node the action attribute belongs to."""
            return int(self._data["node_id"])

        @property
        def attribute_id(self) -> int:
            """Id of the action attribute."""
            return int(self._data["attribute_id"])

        @property
        def source_attribute_id(self) -> int:
            """Id of the source attribute."""
            return int(self.data["source_attribute_id"])

        @property
        def value(self) -> float:
            """Value of the action."""
            return float(self._data["value"])

        @property
        def command(self) -> int:
            """Command type associated with the action."""
            return int(self._data["command"])

    class HomeegramGroupAction(HomeegramAction):
        """Representation of a homeegram group action."""

        @property
        def group_id(self) -> int:
            """Id of the group the action belongs to."""
            return int(self._data["group_id"])

        @property
        def attribute_type(self) -> int:
            """Attribute type of the group action."""
            return int(self._data["attribute_type"])

        @property
        def source_attribute_id(self) -> int:
            """Id of the source attribute."""
            return int(self._data["source_attribute_id"])

        @property
        def value(self) -> float:
            """Value of the action."""
            return float(self._data["value"])

        @property
        def command(self) -> int:
            """Command type associated with the action."""
            return int(self._data["command"])

    class HomeegramNotificationAction(HomeegramAction):
        """Representation of a homeegram notification action."""

        @property
        def style(self) -> int:
            """Style of the notification."""
            return int(self._data["style"])

        @property
        def critical(self) -> bool:
            """Whether the notification is critical."""
            return bool(self._data["critical"])

        @property
        def user_ids(self) -> list[int]:
            """List of user ids to notify."""
            return [int(user_id) for user_id in self._data["user_ids"]]

        @property
        def message(self) -> str:
            """Decoded message of the notification."""
            return unquote(self._data["message"])

    class HomeegramWebhookAction(HomeegramAction):
        """Representation of a homeegram webhook action."""

        @property
        def method(self) -> str:
            """HTTP method of the webhook action."""
            return str(self._data["method"])

        @property
        def url(self) -> str:
            """Decoded URL of the webhook action."""
            return unquote(self._data["url"])

        @property
        def body(self) -> str:
            """Body of the webhook action."""
            return str(self._data["body"])

        @property
        def content_type(self) -> str:
            """Content type of the webhook action."""
            return str(self._data["content_type"])

    class HomeegramHomeegramAction(HomeegramAction):
        """Representation of a homeegram homeegram action."""

        @property
        def target_homeegram_id(self) -> int:
            """Id of the target homeegram for this action."""
            return int(self._data["target_homeegram_id"])

        @property
        def homeegram_event(self) -> int:
            """Homeegram event type for this action."""
            return int(self._data["homeegram_event"])

    def __init__(self, actions: dict[str, Any]) -> None:
        """Initialize actions."""
        self._data = actions

    @property
    def data(self) -> dict[str, list]:
        """Return the raw actions dict."""
        return dict(self._data)

    @property
    def attribute_actions(self) -> list[HomeegramAttributeAction]:
        """Return the list of attribute actions."""
        return [
            self.HomeegramAttributeAction(action)
            for action in self._data["attribute_actions"]
        ]

    @property
    def group_action(self) -> list[HomeegramGroupAction]:
        """Return the list of group actions."""
        return [
            self.HomeegramGroupAction(action) for action in self._data["group_actions"]
        ]

    @property
    def tts_actions(self) -> list[HomeegramTcaItem]:
        # For tts actions I have no information about the structure of
        # the action dict, so I return a list of basic HomeegramTcaItems.
        """Retrun the list of tts actions"""
        return [HomeegramTcaItem(action) for action in self._data["tts_actions"]]

    @property
    def notification_actions(self) -> list[HomeegramNotificationAction]:
        """Return the list of notification actions."""
        return [
            self.HomeegramNotificationAction(action)
            for action in self._data["notification_actions"]
        ]

    @property
    def webhook_actions(self) -> list[HomeegramWebhookAction]:
        """Return the list of webhook actions."""
        return [
            self.HomeegramWebhookAction(action)
            for action in self._data["webhook_actions"]
        ]

    @property
    def homeegram_actions(self) -> list[HomeegramHomeegramAction]:
        """Return the list of homeegram actions."""
        return [
            self.HomeegramHomeegramAction(action)
            for action in self._data["homeegram_actions"]
        ]

    @property
    def plan_actions(self) -> list[HomeegramTcaItem]:
        # For plan actions I have no information about the structure of
        # the action dict, so I return a list of basic HomeegramTcaItems.
        """Retrun the list of plan actions"""
        return [HomeegramTcaItem(action) for action in self._data["plan_actions"]]

    @property
    def user_actions(self) -> list[HomeegramTcaItem]:
        # For user actions I have no information about the structure of
        # the action dict, so I return a list of basic HomeegramTcaItems.
        """Retrun the list of user actions"""
        return [HomeegramTcaItem(action) for action in self._data["user_actions"]]


class HomeeGram(HomeeObject):
    """Representation of a homeegram (automation)."""

    @property
    def id(self) -> int:
        """Id of the homeegram, unique in homee."""
        return int(self._data["id"])

    @property
    def name(self) -> str:
        """Decoded user given name of the homeegram."""
        return unquote(self._data["name"])

    @property
    def image(self) -> str:
        """Image identifier of the homeegram."""
        return unquote(self._data["image"])

    @property
    def state(self) -> int:
        """State of the homeegram."""
        return int(self._data["state"])

    @property
    def visible(self) -> bool:
        """Whether the homeegram is visible."""
        return bool(self._data["visible"])

    @property
    def favorite(self) -> bool:
        """Whether the homeegram is marked as favorite."""
        return bool(self._data["favorite"])

    @property
    def order(self) -> int:
        """Order of the homeegram in the list."""
        return int(self._data["order"])

    @property
    def active(self) -> bool:
        """Whether the homeegram is active."""
        return bool(self._data["active"])

    @property
    def play(self) -> bool:
        """Whether the homeegram is currently playing."""
        return bool(self._data["play"])

    @property
    def added(self) -> int:
        """Timestamp the homeegram was added."""
        return int(self._data["added"])

    @property
    def phonetic_name(self) -> str:
        """Phonetic name of the homeegram."""
        return unquote(self._data["phonetic_name"])

    @property
    def note(self) -> str:
        """Note describing the homeegram."""
        return unquote(self._data["note"])

    @property
    def services(self) -> int:
        """Services associated with the homeegram."""
        return int(self._data["services"])

    @property
    def last_triggered(self) -> int:
        """Time the homeegram was last triggered."""
        return int(self._data["last_triggered"])

    @property
    def owner(self) -> int:
        """Owner id of the homeegram."""
        return int(self._data["owner"])

    @property
    def triggers(self) -> HomeegramTriggers:
        """Dict containing all triggers of the homeegram."""
        return HomeegramTriggers(self._data["triggers"])

    @property
    def conditions(self) -> HomeegramConditions:
        """Dict containing all conditions of the homeegram."""
        return HomeegramConditions(self._data["conditions"])

    @property
    def actions(self) -> HomeegramActions:
        """Dict containing all actions of the homeegram."""
        return HomeegramActions(self._data["actions"])

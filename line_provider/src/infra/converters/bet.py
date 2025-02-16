from uuid import UUID

from domain.commands.bet import NewBetCommand


def convert_new_bet_message_to_command(message: dict) -> NewBetCommand:
    return NewBetCommand(
        event_id=UUID(message["event_id"]),
        bet_amount=float(message["bet_amount"]),
    )

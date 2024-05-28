from pydantic import BaseModel, Extra


class Info(BaseModel, extra=Extra.allow):
    """ Placeholder for showing Info """

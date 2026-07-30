from pydantic import BaseModel, ConfigDict

class BusinessBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        validate_assignment=True,
        use_enum_values=False,
    )

    trace_id: str
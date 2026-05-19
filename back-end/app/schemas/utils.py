def entity_to_schema(entity, schema):
    """
    Converte uma entidade de domínio (POPO) em um schema do Pydantic (DTO/Schema).
    
    Suporta de forma transparente tanto o Pydantic V1 quanto o Pydantic V2,
    checando dinamicamente as propriedades '__fields__' ou 'model_fields'.
    """
    if not entity:
        return None
    fields = schema.__fields__ if hasattr(schema, "__fields__") else schema.model_fields
    return schema(**{k: v for k, v in vars(entity).items() if k in fields})

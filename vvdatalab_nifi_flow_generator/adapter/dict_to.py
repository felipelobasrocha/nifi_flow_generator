def to_processor_data(new_process_group, component_name, component_location, processor_config):
    return type('', (), {
        "new_process_group": new_process_group,
        "component_name": component_name, 
        "component_location": component_location,
        "processor_config": processor_config
    })

def to_connection_data(process_group, source, destination, selected_relationships):
    return type('', (), {
        "process_group": process_group,
        "source": source, 
        "destination": destination,
        "selected_relationships": selected_relationships
    })
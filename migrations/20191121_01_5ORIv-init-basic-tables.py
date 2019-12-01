"""
Init basic tables
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
    CREATE TABLE simulation (
        id BIGSERIAL PRIMARY KEY NOT NULL,
        start_time timestamp NOT NULL)
         """),
    step("""
    CREATE TABLE agent (
        id BIGSERIAL PRIMARY KEY NOT NULL,
        simulation_id BIGINT REFERENCES simulation(id),
        age INT NOT NULL)
         """),
    step("""
    CREATE TABLE point_of_interest (
        id BIGSERIAL PRIMARY KEY NOT NULL,
        simulation_id BIGINT REFERENCES simulation(id),
        x_location INT NOT NULL,
        y_location INT NOT NULL,
        type TEXT NOT NULL,
        properties JSONB NULL)
    """),
    step("""
    CREATE TABLE agent_spacetime_location (
        id BIGSERIAL PRIMARY KEY NOT NULL,
        agent_id BIGINT REFERENCES agent(id),
        simulation_time timestamp NOT NULL,
        x INT NOT NULL,
        y INT NOT NULL,
        point_of_interest_id BIGINT REFERENCES point_of_interest(id) NULL
        )
         """)
]


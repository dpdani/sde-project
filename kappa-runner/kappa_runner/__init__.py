from fastapi import FastAPI


app = FastAPI(
    title="kappa-runner",
    version="0.0.0",
    author="dpdani",
    generate_unique_id_function=lambda route: f"{route.name}",
)

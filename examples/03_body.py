# Step 3: request bodies with Pydantic, response models and status codes.
# A tiny in-memory CRUD API for courses (the data is lost when the server restarts).
# Run:  fastapi dev examples/03_body.py   then try it in /docs
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()


class CourseIn(BaseModel):
    title: str = Field(min_length=3, max_length=80)
    price: float = Field(ge=0)
    tags: list[str] = []


class CourseOut(CourseIn):
    id: int


courses: dict[int, CourseOut] = {}
next_id = 1


@app.post("/courses", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseIn):
    global next_id
    saved = CourseOut(id=next_id, **course.model_dump())
    courses[next_id] = saved
    next_id += 1
    return saved


@app.get("/courses", response_model=list[CourseOut])
def list_courses():
    return list(courses.values())


@app.put("/courses/{course_id}", response_model=CourseOut)
def replace_course(course_id: int, course: CourseIn):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    courses[course_id] = CourseOut(id=course_id, **course.model_dump())
    return courses[course_id]


@app.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int):
    if courses.pop(course_id, None) is None:
        raise HTTPException(status_code=404, detail="Course not found")

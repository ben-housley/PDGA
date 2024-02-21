from classes.hole import Hole

class Layout:
    def __init__(self, data):
        # Mandatory Fields
        self.id = data["LayoutID"]
        self.course_id = data["CourseID"]
        self.course_name = data["CourseName"]
        self.name = data["Name"]
        self.num_holes = data["Holes"]
        self.par = data["Par"]
        self.length = data["Length"]
        self.units = data["Units"]
        self.accuracy = data["Accuracy"]
        self.details = data.get("Details", data.get("Detail", None))

        # Optional Fields
        self.updated_date = data.get("UpdateDate", None)
        self.combined_ssa = data.get("CombinedSSA", None)

        # Methods to call on assignment
        self.set_holes()
        
    def set_holes(self):
        self.holes = []
        for hole in self.details:
            details = hole
            details["layout_id"] = self.id
            details["course_id"] = self.course_id
            self.holes.append(Hole(details))

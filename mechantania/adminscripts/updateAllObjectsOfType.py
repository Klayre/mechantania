# This is how to update all objects of type.

def updateAllObjectsOfType(objTypeClassPath, objTypeClass):
    from objTypeClassPath import objTypeClass

    [obj.at_object_creation() for obj in objTypeClass.objects.all()]

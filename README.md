# ParentFinalizer
This tool is used to quickly assigned parental relationships between a bone and an object parented to it.

Previous attempt:
https://www.youtube.com/watch?v=6tJ-dpK2_V4


Benefits:
- Destruction simulation
- Robots/ Mechanicals
- Abstract rigid movements

Desired automation:
1. mmake an armature, bones, and snap them to selected objects (host)
2. constraints the bones to these objects ( transform mode )
3. bake all bones' movement frames ( optional, only for storing animations from selected objects)
4. create vertex group for each host using the bone´s name
4. remove all constraints on bones
5. combine all hosts into a single object and align the origin point to the armature's.
6. parent all at once (via vertex weight/groups)

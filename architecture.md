
basic architecture of the sample scheduler:

1. main:
   - locate parameter file
   - read in parameters
   - check types of parameters
   - perform any necessary conversions of parameters to objects (like ranges in the dimensions)
   - send parameters to driver
   - catch any propagated errors and write to log before failing
   - receive formatted schedule from driver
   - write schedule to file
	
2. driver:
   - seed the random number generator
   - direct construction of, and collect all of the objects that directly participate in the workflow
   - establish and execute the workflow
   - keep track of number of points selected, logging if it isn't correct
	
3. dispatchers:
   - verify that required parameters are present in the parameters object, log + exception if missing parameters
   - maintain list of modules implementing that interface
   - use modules to construct implementing object upon request (from parameters object)
	
4. implementers:
   - assume that parameters passed are correct in type and value
   - provide a function that returns an implementing object (or some other means of implementing that object)
	
	
5. other:
   - put parameters object into WrappedDictionary which provides logging + exception in the case of missing parameters
	
6. goals (that may or may not have been achieved):
   - fail during construction of implementing objects, or don't fail at all
   - provide a log that is instructive and helpful in case of a failure or unexpected result
   - provide helpful error messages in the case of receiving bad parameters 
     - missing parameter
     - wrong type
     - wrong value
     - extra (unused) parameter
	
	
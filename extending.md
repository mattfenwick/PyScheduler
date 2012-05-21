Extending the Sample Scheduler

1. adding a new workflow
   - the current workflow is in the Driver module

2. adding a new implementing module
   - for the corresponding package:
     - create the module in the correct package
     - in the Dispatcher module
       - import the new module
       - write a function which:
         - extracts the appropriate parameters from a dictionary 
         - uses the extracted parameters to call the new module and construct an implementing object
       - add this function to the dictionary -- PROBLEM where is this dictionary located in general??
     - add unittests in the TestSuite module of the package, making sure that they are included when automated tests are run

3.  adding a new parameter
   - if early type-checking of the parameter is desired
     - modify typeCheck/dimensionTypeCheck method in Parameters
   - add to types/dimensionTypes table in Parameters
   - adding a parameter to the type-checkers also allows for an automatically generated overview which
     - describes the various parameters and their restrictions
	
4.  adding a new stage in a workflow
   - create a name for a parameter which describes the stage
     - add this parameter to the 'types' table in Parameters
   - create a new package
   - create a Dispatcher module
     - define an interface for the package in the doc string (__doc__, or triple-quoted string at top of file)
     - the Dispatcher module is responsible for converting the user-defined parameters into the appropriate object that implements the package's interface
     - create a 'getObject' method that accepts a dictionary of parameters and returns the correct implementing object
     - create a method 'getImplementingModules' that returns an iterable of the modules in the package
     - create a dictionary 'implementingModules' whose keys are the names that a user must enter in order to use that algorithm, and whose values include the corresponding modules (in most cases, the value also includes the method in Dispatcher that uses that module)
     - wrap the dictionary using Utilities.WrappedDictionary, and provide it with an error message and the name of the parameter, which allows for error reporting which tells the user which parameter was wrong and what the enumeration of correct values is 
   - create implementing modules
     - describe the required parameters and the implemented algorithm in each module's __doc__ attribute
     - make sure to distinguish between parameters that are required for each dimension and those that are not
   - write unittests and workflow tests

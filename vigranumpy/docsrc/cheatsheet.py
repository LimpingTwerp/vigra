import numpy
import vigra

#__________________________________creation_____________________________________

#        we start with a numpy.ndarray, of the dimensions 100,100,3

numpyArray = numpy.ndarray((100,100,3)) 

#        theres is an ambiguity in the meaning of the dimeinsions, the third 
#        dimension could either be a channel 'c' or simply the third spacial
#        dimension 'z'. To clarify this we assign a vigra.AxisTags-Object to 
#        the numpyArray while we convert it into a vigra.VigraArray.
#        vigra.AxisTags and the vigra.AxisInfo objects corresponding to the 
#        dimensions of the numpy.ndarray are created thus:

axisTags = vigra.AxisTags()

#        Here the key-property is the 'name' of the axis or dimension, the 
#        typeFlags property set the type of the dimension (Time, Space, Channel)
#        resolution is self explaining ('0.0' means unknown resolution), 
#        description is also self explaining

xAxisInfo = vigra.AxisInfo(key='x',typeFlags=vigra.AxisType.Space,resolution=0.0,description="")  
yAxisInfo = vigra.AxisInfo(key='y',typeFlags=vigra.AxisType.Space,resolution=0.0,description="")  
cAxisInfo = vigra.AxisInfo(key='c',typeFlags=vigra.AxisType.Channels,resolution=0.0,description="")  

#        at this point we insert the vigra.AxisInfo objects in the 
#        vigra.axisTags object. The order of insertion is determined by the 
#        integer variable and must correspond the the order of the dimensions in
#        the numyp.ndarray.

axisTags.insert(0,xAxisInfo)
axisTags.insert(1,yAxisInfo)
axisTags.insert(2,cAxisInfo)

#        equivalently

axisTags = vigra.AxisTags(xAxisInfo,yAxisInfo,cAxisInfo)

#        now the AxisTags-object is ready to be merged with the numpy.ndarray 
#        into a vigra.VigraArray. The order property sets the order of the axis
#        according to the canical order of different models ('C' - C-order, 'F'
#        - Fortran, 'A'-Any). If it is set to None, the order will be as set in
#        vigraArray.defaultOrder

vigraArray = vigra.VigraArray(numpyArray,axistags=axisTags, order=None)

#        The information about the axis can be retrieved thus:

vigraArray.axistags

#        a quick way to create a vigra array with default AxisTags is:

vigraArrayQuick = vigra.VigraArray((100,100,100,3))

#______________________retrieving and setting information_______________________

#        Once the AxisTags are assigned to a vigra.VigraArray, they can be
#        manipulated and their structure accessed in the following ways:

#GET the CURRENT POSITION of any given AXIS
vigraArray.axistags.index('y')
vigraArray.axistags.index('c')
vigraArray.axistags.index('Nonsense') #this will return dim(vigrArray), '3' in this case

vigraArray.axistags.channelIndex #get the current position of the channel 'axis'
vigraArray.channelIndex

#GET the NUBER of different AXISTYPES
vigraArray.axistags.axisTypeCount(vigra.AxisType.Space)
vigraArray.spatialDimensions 

#SET the the RESOLUTION and DESCRIPTION of the AxisInfo-object and the 
#description of the AxisInfo corresponding to the channel axis 

vigraArray.axistags.setDescription('x','x-Axis')
vigraArray.axistags.setDescription(1,'y-Axis')

vigraArray.axistags.setResolution(0,1.6)
vigraArray.axistags.setResolution('y',2.6)

vigraArray.axistags.setChannelDescription('RGB')

#GET information about the MAGNITUDE of the respective DIMENSION

vigraArray.width    #always the Axis designated as key='x'
vigraArray.height   #always the Axis designated as key='y'

#         This will raise a runtimerror, because there are no axis with the specified 
#         key in our example'

try:
    vigraArray.depth    #always the Axis designated as key='z'
    vigraArray.channels #always the Axis designated as key='c'
    vigraArray.duration #always the Axis designated as key='t'
except:
    pass

#_______________________________manipulation____________________________________

#            Axis can be added, so that the existing volume will be viewed as 
#            the 'slice' slice of a higher dimensional volume. The reversed 
#            process can be imagined as the projection of the original volume on
#            a subvolume. The original volume has to be reduced to a specific 
#            'slice' in the dimension which is to be dropped, since there are 
#            many 'slices'.

#thus you ADD AXIS:
#vigraArray.shape = (100,100,3)
vigraArray = vigraArray.withAxes('x','y','z','c')
#vigraArray.shape = (100,100,1,3)


#thus you REMOVE AXIS:
#vigraArray.shape = (100,100,3)
vigraArray = vigraArray[...,0]  
vigraArray = vigraArray.withAxes('x','y')
#vigraArray.shape = (100,100)


#thus you ADD and REMOVE the CHANNELAXIS:
#vigraArray.shape = (100,100)
vigraArray=vigraArray.insertChannelAxis()
#vigraArray.shape = (100,100,1)
vigraArray=vigraArray.dropChannelAxis(ignoreMultiChannel=True) 
#vigraArray.shape = (100,100)

#        this way it is possible to get any projection

vigraArray = vigra.VigraArray((100,100,100,3))
vigraArray = vigraArray[:,50,:,1]
vigraArray = vigraArray.withAxes('x','z')

#        another way to do the same thing is

vigraArray = vigra.VigraArray((100,100,100,3))
vigraArray = vigraArray.bindAxis('y', 50)
vigraArray = vigraArray.bindAxis('c', 1)

#        there is not direct way to extend the volumes. It is possible to use 
#        the copy function, though. Suppose we have a one channel picture and 
#        want to add 2 channels:

vigraArray = vigra.VigraArray((100,100,1))
vigraArrayExtended = vigra.VigraArray((100,100,3))
vigraArrayExtended[:,:,0].copyValues(vigraArray)


#        the axis can be permuted. The types of order are:
#        'A' - Any order. The identity permutation 
#        'C' - The C order. z y x c
#        'F' - The Fortran order. c x y z
#        'V' - The Vigra order. x y z c

#        a quick way to get any AxisTags order needed is the defaultAxistags()
#        method:

vigraArray = vigra.VigraArray(numpy.ndarray((100,100,100)),axistags = vigra.VigraArray.defaultAxistags('yzx'))
#order : y z x

#which can be rearranged if needed
vigraArray = vigraArray.transposeToVigraOrder()
#order : x y z
        

#        it is possible to get ITERATORS which iterate over a given axis (space-
#        axis, time-axis,channel-axis). There is also the possibility to just 
#        iterate over the space-volume alone or just over two dimensional slices

vigraArray = vigra.VigraArray((20,100,100,100,3))

#CHANNEL iterator
timeIterator = vigraArray.channelIter()

#TIME iterator
timeIterator = vigraArray.timeIter()

#SPACE iterator (for x in xDim: for y in yDim: for z in zDim: (time,channel))
spaceIterator = vigraArray.spaceIter()

#SPACE iterator over SLICES along an axis:
zSliceIterator = vigraArray.sliceIter('z')

#WEBSITE: http://hci.iwr.uni-heidelberg.de/vigra/doc/vigranumpy/index.html
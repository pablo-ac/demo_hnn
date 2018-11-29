from netpyne import specs, sim
import sys

#interface paramsfirst
print(sys.argv[1])
print(sys.argv[2])
evoked_rate=sys.argv[1]
evoked_start=sys.argv[2]

# Network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

netParams.sizeX = 100 # x-dimension (horizontal length) size in um
netParams.sizeY = 500 # y-dimension (vertical height or cortical depth) size in um
netParams.sizeZ = 100 # z-dimension (horizontal length) size in um
netParams.propVelocity = 100.0 # propagation velocity (um/ms)
netParams.probLengthConst = 40.0 # length constant for conn probability (um)

## Population parameters
netParams.popParams['E2'] = {'cellType': 'E', 'yRange': [200,201], 'cellModel': 'HH', 'gridSpacing': 10}
netParams.popParams['I2'] = {'cellType': 'I', 'yRange': [200,201], 'cellModel': 'HH', 'gridSpacing': 20}
netParams.popParams['E5'] = {'cellType': 'E', 'yRange': [400,401], 'cellModel': 'HH', 'gridSpacing': 10}
netParams.popParams['I5'] = {'cellType': 'I', 'yRange': [400,401], 'cellModel': 'HH', 'gridSpacing': 20}


## Cell property rules
### E cells
netParams.loadCellParamsRule(label='Erule', fileName='IT2_reduced_cellParams.json')
netParams.cellParams['Erule']['conds'] = {'cellType': ['E']}

### I cells
cellRule = {'conds': {'cellType': 'I'},  'secs': {}}  # cell rule dict
cellRule['secs']['soma'] = {'geom': {}, 'mechs': {}}                              # soma params dict
cellRule['secs']['soma']['geom'] = {'diam': 10.0, 'L': 9.0, 'Ra': 110.0, 'nseg': 1}                  # soma geometry
cellRule['secs']['soma']['mechs']['hh'] = {'gnabar': 0.11, 'gkbar': 0.036, 'gl': 0.003, 'el': -70}      # soma hh mechanism
cellRule['secs']['soma']['weightNorm'] = [0.0001]
netParams.cellParams['Irule'] = cellRule                          # add dict to list of cell params


## Synaptic mechanism parameters
netParams.synMechParams['exc'] = {'mod': 'Exp2Syn', 'tau1': 0.8, 'tau2': 5.3, 'e': 0}  # NMDA synaptic mechanism
netParams.synMechParams['inh'] = {'mod': 'Exp2Syn', 'tau1': 0.6, 'tau2': 8.5, 'e': -75}  # GABA synaptic mechanism

## Stimulation parameters
netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': 10, 'noise': 1.0}
netParams.stimSourceParams['evoked'] = {'type': 'NetStim', 'rate': evoked_rate, 'noise': 0.5, 'start': evoked_start, 'number': 20}

### proximal
netParams.stimTargetParams['bkg_proximal'] = {
    'source': 'bkg', 
    'conds': {'cellType': ['E','I']}, 
    'weight': 10.0, 
    'sec': ['soma', 'Bdend'], 
    'delay': 1, 
    'synMech': 'exc'}

### distal
netParams.stimTargetParams['bkg_distal'] = {
    'source': 'bkg', 
    'conds': {'cellType': ['E']}, 
    'weight': 10.0, 
    'sec': 'apicdend', 
    'delay': 1, 
    'synMech': 'exc'}

### evoked
netParams.stimTargetParams['evoked_E2'] = {
    'source': 'evoked', 
    'conds': {'pop': 'E2'}, 
    'weight': 10.0, 
    'sec': 'apicdend', 
    'delay': 1, 
    'synMech': 'exc'}


## Cell connectivity rules
### E2->E2
netParams.connParams['E2->E2'] = {
  'preConds': {'pop': 'E2'}, 
  'postConds': {'pop': 'E2'},         
  'weight': '1*exp(-dist_2D/probLengthConst)',      
  'delay': 'dist_3D/propVelocity',     
  'sec': ['soma', 'Bdend'],
  'synMech': 'exc'}                   

### E2->E5
netParams.connParams['E2->E5'] = {
  'preConds': {'pop': 'E2'}, 
  'postConds': {'pop': 'E5'},         
  'weight': '0.5*exp(-dist_2D/probLengthConst)',         
  'delay': 'dist_3D/propVelocity',      
  'sec': 'alldend',
  'synMech': 'exc'}                 
                     
### E2->I2
netParams.connParams['E2->I2'] = {
  'preConds': {'pop': 'E2'}, 
  'postConds': {'pop': 'I2'},       
  'weight': '1*exp(-dist_2D/probLengthConst)',        
  'delay': 'dist_3D/propVelocity',                  
  'synMech': 'exc'}                              

### I2->E2/I2
netParams.connParams['I2->E2'] = {
  'preConds': {'pop': 'I2'}, 
  'postConds': {'pop': ['E2', 'I2']},       
  'weight': '2*exp(-dist_2D/probLengthConst)',                                     
  'delay': 'dist_3D/propVelocity',  
  'sec': ['soma'],                    
  'synMech': 'inh'}                                  

### E5->E5
netParams.connParams['E5->E5'] = {
  'preConds': {'pop': 'E5'}, 
  'postConds': {'pop': 'E5'},     
  'weight': '1*exp(-dist_2D/probLengthConst)',                                     
  'delay': 'dist_3D/propVelocity',                      
  'sec': ['soma', 'Bdend'],
  'synMech': 'exc'}                                    

### E5->I5
netParams.connParams['E5->I5'] = {
  'preConds': {'pop': 'E5'}, 
  'postConds': {'pop': 'I5'},      
  'weight': '1*exp(-dist_2D/probLengthConst)',                                     
  'delay': 'dist_3D/propVelocity',                     
  'synMech': 'exc'}                                   

### I5->E5/I5
netParams.connParams['I5->E5/I5'] = {
  'preConds': {'pop': 'I5'}, 
  'postConds': {'pop': ['E5','I5']},      
  'weight': '2*exp(-dist_2D/probLengthConst)',                                      
  'delay': 'dist_3D/propVelocity',
  'sec': ['soma'],                      
  'synMech': 'inh'}    


# Simulation configuration
simConfig = specs.SimConfig()        # object of class SimConfig to store simulation configuration
simConfig.duration = 1.0*1e3           # Duration of the simulation, in ms
simConfig.dt = 0.1                # Internal integration timestep to use
simConfig.verbose = False            # Show detailed messages 
simConfig.recordStep = 1             # Step size in ms to save data (eg. V traces, LFP, etc)
simConfig.filename = 'model'   # Set file output name

simConfig.recordLFP = [[-15, y, 1.0*netParams.sizeZ] for y in range(int(netParams.sizeY/5.0), int(netParams.sizeY), int(netParams.sizeY/5.0))]

simConfig.analysis['plotRaster'] = {'orderBy': 'y', 'orderInverse': True, 'saveFig':True, 'figSize': (9,3)}      # Plot a raster
simConfig.analysis['plotSpikeStats'] = {'saveFig': True}
simConfig.analysis['plotLFP'] =  {'includeAxon': False, 'figSize': (6,10), 'NFFT': 256, 'noverlap': 48, 'nperseg': 64, 'saveFig': True} 

#simConfig.analysis['plotRaster'] = {'saveFig': True}
#simConfig.analysis['plotSpikeStats'] = {'saveFig': True}
#simConfig.analysis['plotLFP'] = {'saveFig': True}


# Create network and run simulation
sim.createSimulateAnalyze(netParams = netParams, simConfig = simConfig)    

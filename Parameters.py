######################################################### pacing mode parameters
limits = ['Lower Rate Limit', 'Upper Rate Limit']
A = ['Atrial Amplitude', 'Atrial Pulse Width'] 
V = ['Ventricular Amplitude', 'Ventricular Pulse Width'] 

AOOParameters = limits + A
VOOParameters = limits + V
AAIParameters = limits + A + ['Atrial Sensitivity','ARP','PVARP','Hysteresis','Rate Smoothing'] 
VVIParameters = limits + V + ['Ventricular Sensitivity','VRP','Hysteresis','Rate Smoothing'] 
DOOParameters = limits + A + V + ['Fixed AV Delay'] 

######################################################### parameter values
tp1 = tuple( [str(x) for x in range(30,55,5)])
tp2 = tuple( [str(x) for x in range(51,91)] )
tp3 = tuple( [str(x) for x in range(95,180,5)] )

tp4 = tuple( [str(x) for x in range(50,180,5)] )
tp5 = tuple(["0.05"]) + tuple( [str(x/10) for x in range(1,20,1)] )
tp6 = tuple( ["off"] + [str(x/10) for x in range(5,33,1)] + [str(x/10) for x in range(35,75,5)] )

tp7 = tuple( ["0.25","0.5","0.7"] + [str(x/10) for x in range(1,11,1)])
tp8 = tuple( [str(x) for x in range(150,510,10)] )
tp9 = tuple(["off"] + [str(x) for x in range(3,24,3)] + ["25"])

tp10 = ("V-Low","Low","Med-Low","Med","Med-High","High","V-High")
tp11 = tuple([str(x) for x in range(10,60,10)])
tp12 = tuple([str(x) for x in range(1,17)])
tp13 = tuple([str(x) for x in range(2,17)])
tp14 = tuple([str(x) for x in range(70,310,10)])

ParameterValues =	{
"Lower Rate Limit": [tp1 + tp2 + tp3,"60"],
"Upper Rate Limit": [tp4,"120"],
"Atrial Amplitude": [tp6,"3.5"],
"Atrial Pulse Width": [tp5,"0.4"],
"Ventricular Amplitude": [tp6,"3.5"],
"Ventricular Pulse Width": [tp5,"0.5"],
"Atrial Sensitivity": [tp7,"0.75"],
"ARP": tp8,
"PVARP": tp8,
"Hysteresis": tuple(["off"]) + tp1 + tp2 + tp3,
"Rate Smoothing": tp9,
"Ventricular Sensitivity": [tp7,"2.5"],
"VRP": [tp8,"320"],
"Maximum Sensor Rate": [tp4,"120"],
"Activity Threshold": [tp10,"Med"],
"Reaction Time": [tp11,"30"],
"Response Factor": [tp12,"8"],
"Recovery Time": [tp13,"5"],
"Fixed AV Delay": [tp14,"150"]
}
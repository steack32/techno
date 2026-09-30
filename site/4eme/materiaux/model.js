// Modèle pédagogique : poutre simplement appuyée, charge ponctuelle centrale.
// Petites déformations élastiques ; poids propre et assemblages non modélisés.
export const materials={
 bois:{name:'Bois, fibres dans la longueur',E:10e9,rho:600,color:'#c89357'},
 aluminium:{name:'Aluminium',E:69e9,rho:2700,color:'#94a8b9'},
 acier:{name:'Acier',E:200e9,rho:7850,color:'#587084'}
};
export function calculate({material='bois',span=80,thickness=15,shape='plein',load=10}={}){
 if(!materials[material]||![40,60,80,100].includes(Number(span))||![10,15,20,25,30].includes(Number(thickness))||!['plein','creux'].includes(shape)||![0,5,10,15,20].includes(Number(load)))throw Error('Réglage non valide');
 if(material==='bois'&&shape==='creux')throw Error('Le bois est étudié avec une section pleine.');
 const m=materials[material],L=Number(span)/100,h=Number(thickness)/1000,b=.25,t=.0015;
 const A=shape==='plein'?b*h:b*h-(b-2*t)*(h-2*t);
 const I=shape==='plein'?b*h**3/12:(b*h**3-(b-2*t)*(h-2*t)**3)/12;
 const force=Number(load)*9.81,deflection=force*L**3/(48*m.E*I)*1000,mass=m.rho*A*L;
 return {deflection,mass,I,A,force,valid:deflection<=L*1000/100,pass:deflection<=3&&mass<=2&&Number(span)===80&&Number(load)===10};
}

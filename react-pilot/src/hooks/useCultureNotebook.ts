import {useEffect, useState} from 'react';
import catalog from '../data/events.json';

const STORAGE_KEY='ehime-v2-culture-notes';
const validIds=new Set(catalog.map(e=>e.id));
function sanitize(value:unknown):string[]{
  return Array.isArray(value)?Array.from(new Set(value.filter((id):id is string=>typeof id==='string'&&validIds.has(id)))):[];
}
export function useCultureNotebook(){
  const [saved,setSaved]=useState<string[]>([]);
  const [storageAvailable,setStorageAvailable]=useState(true);
  useEffect(()=>{
    try{setSaved(sanitize(JSON.parse(localStorage.getItem(STORAGE_KEY)||'[]')))}
    catch{setStorageAvailable(false)}
  },[]);
  const toggleSaved=(id:string)=>{
    if(!validIds.has(id))return;
    setSaved(prev=>{
      const next=prev.includes(id)?prev.filter(k=>k!==id):[...prev,id];
      try{localStorage.setItem(STORAGE_KEY,JSON.stringify(next))}
      catch{setStorageAvailable(false)}
      return next;
    });
  };
  return {saved,storageAvailable,toggleSaved};
}

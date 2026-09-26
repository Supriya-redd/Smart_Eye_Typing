"""EyeType gaze typing using MediaPipe Tasks and 1.3-second gaze dwell."""
import tkinter as tk
from tkinter import ttk,messagebox
import cv2,mediapipe as mp
from PIL import Image,ImageTk
from pathlib import Path
import urllib.request,time
MODEL_URL="https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
MODEL=Path(__file__).with_name("face_landmarker.task")
BG="#F6F3FB"; PANEL="#E9E2F3"; DARK="#FFFFFF"; KEY="#D8E9E4"; ACCENT="#B9C9EA"; ACCENT_TEXT="#68769B"; TEXT="#29343A"; MUTED="#56666C"
class EyeType:
 def __init__(self,root):
  self.root=root;root.title("EyeType — Accessible Gaze Typing");root.geometry("1120x790");root.minsize(950,700);root.configure(bg=BG)
  self.cap=None;self.detector=None;self.running=False;self.gaze=None;self.cal=None;self.samples=None;self.points={};self.step=0;self.current=None;self.keys=[];self.last_ms=0;self.pointer_xy=None;self.dwell=1.3;self.current_started=None;self.activated=False
  ttk.Style().theme_use("clam");ttk.Style().configure("TButton",font=("Segoe UI",11),padding=8)
  top=tk.Frame(root,bg=BG);top.pack(fill="x",padx=24,pady=14)
  tk.Label(top,text="EyeType",font=("Segoe UI",27,"bold"),fg=TEXT,bg=BG).pack(side="left")
  tk.Label(top,text="ACCESSIBLE COMMUNICATION",font=("Segoe UI",10,"bold"),fg=ACCENT_TEXT,bg=BG).pack(side="left",padx=15,pady=(12,0))
  row=tk.Frame(root,bg=BG);row.pack(fill="both",expand=True,padx=22)
  self.preview=tk.Label(row,text="Start camera, calibrate, then look at a key",font=("Segoe UI",13),fg=MUTED,bg=DARK,width=64,height=16);self.preview.pack(side="left",fill="both",expand=True,padx=(0,14))
  side=tk.Frame(row,bg=PANEL,width=280);side.pack(side="right",fill="y");side.pack_propagate(False)
  tk.Label(side,text="GET STARTED",font=("Segoe UI",11,"bold"),fg=ACCENT_TEXT,bg=PANEL).pack(anchor="w",padx=16,pady=(18,8))
  ttk.Button(side,text="Start / Stop camera",command=self.toggle_camera).pack(fill="x",padx=14,pady=5)
  ttk.Button(side,text="Calibrate gaze",command=self.calibrate).pack(fill="x",padx=14,pady=5)
  for t in ("1. Face the camera in even lighting.","2. Calibrate by looking left, right, up, then down.","3. Look at a key and keep your gaze steady.","4. It types after 1.3 seconds; look away for the next key."):
   tk.Label(side,text=t,wraplength=238,justify="left",fg=TEXT,bg=PANEL,font=("Segoe UI",10)).pack(anchor="w",padx=16,pady=7)
  ttk.Button(side,text="Speak message",command=self.speak).pack(fill="x",padx=14,pady=(12,5))
  self.status=tk.StringVar(value="Start the camera to begin.")
  tk.Label(root,textvariable=self.status,anchor="w",fg=TEXT,bg=BG,font=("Segoe UI",10)).pack(fill="x",padx=25,pady=8)
  panel=tk.Frame(root,bg=PANEL);panel.pack(fill="x",padx=22,pady=(0,8))
  tk.Label(panel,text="YOUR MESSAGE",font=("Segoe UI",10,"bold"),fg=ACCENT_TEXT,bg=PANEL).pack(anchor="w",padx=12,pady=(9,3))
  self.text=tk.Text(panel,height=2,font=("Segoe UI",17),bg=DARK,fg=TEXT,insertbackground=TEXT,relief="flat",padx=8,pady=6);self.text.pack(fill="x",padx=10)
  actions=tk.Frame(panel,bg=PANEL);actions.pack(fill="x",padx=10,pady=7)
  for label,fn in (("Space",lambda:self.insert(" ")),("⌫ Backspace",self.backspace),("Clear",self.clear)):ttk.Button(actions,text=label,command=fn).pack(side="left",padx=(0,6))
  self.keyboard=tk.Frame(root,bg=BG);self.keyboard.pack(fill="x",padx=18,pady=(0,12))
  for rowstr in ("QWERTYUIOP","ASDFGHJKL","ZXCVBNM"):
   band=tk.Frame(self.keyboard,bg=BG);band.pack(pady=2)
   for c in rowstr:self.makekey(band,c,lambda c=c:self.insert(c.lower()),5)
  band=tk.Frame(self.keyboard,bg=BG);band.pack(pady=2)
  for c,w,fn in (("SPACE",18,lambda:self.insert(" ")),("⌫",7,self.backspace),("ENTER",9,lambda:self.insert("\n"))):self.makekey(band,c,fn,w)
  root.protocol("WM_DELETE_WINDOW",self.close)
 def makekey(self,parent,label,cmd,width):
  b=tk.Button(parent,text=label,width=width,height=2,font=("Segoe UI",12,"bold"),fg=TEXT,bg=KEY,activebackground=ACCENT,relief="flat",command=cmd);b.pack(side="left",padx=3);self.keys.append(b)
 def toggle_camera(self):
  if self.running:self.stop();return
  try:
   if not MODEL.exists():self.status.set("Downloading face landmark model once…");self.root.update_idletasks();urllib.request.urlretrieve(MODEL_URL,str(MODEL))
   opts=mp.tasks.vision.FaceLandmarkerOptions(base_options=mp.tasks.BaseOptions(model_asset_path=str(MODEL)),running_mode=mp.tasks.vision.RunningMode.VIDEO,num_faces=1)
   self.detector=mp.tasks.vision.FaceLandmarker.create_from_options(opts);self.cap=cv2.VideoCapture(0)
   if not self.cap.isOpened():raise RuntimeError("Camera could not be opened")
   self.running=True;self.status.set("Camera active. Calibrate gaze before typing.");self.frame()
  except Exception as e:self.stop();messagebox.showerror("Camera unavailable",str(e))
 def stop(self):
  self.running=False
  if self.cap:self.cap.release();self.cap=None
  if self.detector:self.detector.close();self.detector=None
 def frame(self):
  if not self.running:return
  ok,frame=self.cap.read()
  if ok:
   frame=cv2.flip(frame,1);rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB);img=mp.Image(image_format=mp.ImageFormat.SRGB,data=rgb)
   ms=max(int(time.monotonic()*1000),self.last_ms+1);self.last_ms=ms;res=self.detector.detect_for_video(img,ms)
   if res.face_landmarks:
    lm=res.face_landmarks[0];self.gaze=self.eye_position(lm)
    cv2.putText(frame,"GAZE TRACKING ACTIVE",(12,26),cv2.FONT_HERSHEY_SIMPLEX,.58,(70,160,120),2)
    if self.samples is not None:self.samples.append(self.gaze)
    elif self.cal:
     self.choose_key()
   else:cv2.putText(frame,"FACE NOT FOUND - adjust light/distance",(12,26),cv2.FONT_HERSHEY_SIMPLEX,.5,(20,80,255),2)
   im=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB));im.thumbnail((700,480));pic=ImageTk.PhotoImage(im);self.preview.configure(image=pic,text="");self.preview.image=pic
  self.root.after(25,self.frame)
 @staticmethod
 def eye_position(lm):
  def hr(i,a,b):return (lm[i].x-min(lm[a].x,lm[b].x))/max(abs(lm[a].x-lm[b].x),1e-5)
  def vr(i,a,b):return (lm[i].y-min(lm[a].y,lm[b].y))/max(abs(lm[a].y-lm[b].y),1e-5)
  return ((hr(468,33,133)+hr(473,362,263))/2,(vr(468,159,145)+vr(473,386,374))/2)
 def calibrate(self):
  if not self.running:self.status.set("Start camera before calibration.");return
  self.points={};self.step=0;self.prompt()
 def prompt(self):
  dirs=("left","right","up","down")
  if self.step==4:
   self.cal=(self.points["left"][0],self.points["right"][0],self.points["up"][1],self.points["down"][1]);self.status.set("Calibration complete. Hold your gaze on a key for 1.3 seconds to type it.");return
  d=dirs[self.step];messagebox.showinfo("Gaze calibration",f"Look {d.upper()} as far as comfortable. Keep your head still. Press OK and hold for one second.")
  self.samples=[];self.root.after(1100,lambda:self.record(d))
 def record(self,d):
  vals=self.samples or [];self.samples=None
  if len(vals)<5:self.status.set("Eyes not tracked long enough. Retry calibration in brighter light.");return
  self.points[d]=(sum(x for x,y in vals)/len(vals),sum(y for x,y in vals)/len(vals));self.step+=1;self.prompt()
 def choose_key(self):
  xl,xr,yu,yd=self.cal
  if abs(xr-xl)<.025 or abs(yd-yu)<.025:return
  gx=max(0,min(1,(self.gaze[0]-xl)/(xr-xl)));gy=max(0,min(1,(self.gaze[1]-yu)/(yd-yu)))
  self.root.update_idletasks()
  kb=self.keyboard;rawx=kb.winfo_rootx()+gx*kb.winfo_width();rawy=kb.winfo_rooty()+gy*kb.winfo_height()
  if self.pointer_xy is None:self.pointer_xy=(rawx,rawy)
  else:
   cx,cy=self.pointer_xy;dx=max(-4.0,min(4.0,(rawx-cx)*.08));dy=max(-4.0,min(4.0,(rawy-cy)*.08))
   self.pointer_xy=(cx+dx,cy+dy)
  px,py=self.pointer_xy
  target=min(self.keys,key=lambda b:(b.winfo_rootx()+b.winfo_width()/2-px)**2+(b.winfo_rooty()+b.winfo_height()/2-py)**2)
  if target is not self.current:
   self.current=target;self.current_started=time.monotonic();self.activated=False
   for b in self.keys:b.configure(bg=KEY)
   target.configure(bg=ACCENT)
  elapsed=time.monotonic()-self.current_started
  if not self.activated and elapsed>=self.dwell:
   self.current.invoke();self.activated=True
   self.status.set(f"Typed {self.current.cget('text')}. Look at another key to continue.")
  elif not self.activated:
   self.status.set(f"{target.cget('text')} highlighted — typing in {max(0,self.dwell-elapsed):.1f}s")
 def insert(self,s):self.text.insert("insert",s)
 def backspace(self):
  i=self.text.index("insert")
  if i!="1.0":self.text.delete(f"{i}-1c",i)
 def clear(self):self.text.delete("1.0","end")
 def speak(self):
  msg=self.text.get("1.0","end-1c").strip()
  if not msg:return
  try:import pyttsx3;e=pyttsx3.init();e.say(msg);e.runAndWait()
  except Exception as ex:messagebox.showerror("Speech unavailable",str(ex))
 def close(self):self.stop();self.root.destroy()
if __name__=="__main__":
 root=tk.Tk();EyeType(root);root.mainloop()

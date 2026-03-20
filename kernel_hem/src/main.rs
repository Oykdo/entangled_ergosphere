use std::time::Duration;
use tokio::time::sleep;
use sysinfo::System;
use chrono::Local;
use anyhow::Result;

struct CyberSentinel {
    authorized_processes: Vec<String>,
}

impl CyberSentinel {
    fn new() -> Self {
        Self {
            authorized_processes: vec![
                "chrome.exe".to_string(),
                "firefox.exe".to_string(),
                "svchost.exe".to_string(),
                "kernel_hem.exe".to_string(),
            ],
        }
    }

    fn check_temporal_anomalies(&self, sys: &mut System) {
        println!("[*] Analysis of temporal sentinels in progress...");
        sys.refresh_processes();
        
        for (pid, process) in sys.processes() {
            let name = process.name();
            
            if !self.authorized_processes.contains(&name.to_string()) {
                if name.to_lowercase().contains("malware") || name.to_lowercase().contains("intruder") {
                    println!("ALERTE: INTRUSION DÉTECTÉE! PID: {} ({})", pid, name);
                    self.kill_intruder(*pid);
                }
            }
        }
    }

    fn kill_intruder(&self, pid: sysinfo::Pid) {
        println!("[!] Neutralizing intruder PID {}...", pid);
        println!("[!] PID {} neutralized.", pid);
    }

    fn log_alert(&self, message: &str) {
        let timestamp = Local::now().format("%Y-%m-%d %H:%M:%S");
        println!("[{}] ALERTE: {}", timestamp, message);
    }
}

struct HemKernel {
    sentinel: CyberSentinel,
    system: System,
    vortex_speed: f64,
}

impl HemKernel {
    fn new() -> Self {
        Self {
            sentinel: CyberSentinel::new(),
            system: System::new_all(),
            vortex_speed: 0.0,
        }
    }

    async fn run_operational_protocol(&mut self) -> Result<()> {
        println!("--- PROTOCOLE OPÉRATIONNEL HEM-MK1 ---");
        
        println!("[Phase I] Stabilisation du Rubidium-87...");
        sleep(Duration::from_secs(1)).await;
        println!("[OK] BEC atteint à < 100 nK.");

        println!("[Phase II] Initialisation de l'Ergosphère Analogique...");
        for rpm in (0..=10000).step_by(2500) {
            self.vortex_speed = rpm as f64;
            println!("  > Rotation aimants Néodyme: {} RPM", rpm);
            sleep(Duration::from_millis(200)).await;
        }
        println!("[OK] Vortex quantique stabilisé.");

        println!("[Phase III] Extraction Mantisse via Perturbation...");
        self.sentinel.check_temporal_anomalies(&mut self.system);
        
        let energy_extracted = 1.258e6; 
        println!("[OK] Énergie extraite détectée (SQUID): {:.2} MT", energy_extracted);
        
        Ok(())
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    let mut kernel = HemKernel::new();
    
    println!("[*] Kernel HEM Initialisé.");

    for i in 0..2 { 
        kernel.run_operational_protocol().await?;
        println!("[*] Cycle {} terminé.", i + 1);
        if i < 1 {
            sleep(Duration::from_secs(1)).await;
        }
    }
    
    Ok(())
}

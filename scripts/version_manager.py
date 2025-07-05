#!/usr/bin/env python3
"""
QDPI Version Management (oren_progresso)
Semantic versioning for codex, flows, and UI components
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

class QDPIVersionManager:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.version_file = self.repo_path / "VERSION.json"
        
    def get_current_version(self) -> dict:
        """Get current version info"""
        if self.version_file.exists():
            with open(self.version_file) as f:
                return json.load(f)
        
        return {
            "major": 1,
            "minor": 0,
            "patch": 0,
            "codex_version": "1.0.0",
            "flows_version": "1.0.0",
            "ui_version": "1.0.0",
            "api_version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "commit": self._get_commit_hash(),
            "changes": {}
        }
    
    def _get_commit_hash(self) -> str:
        """Get current commit hash"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return "unknown"
    
    def _get_last_tag(self) -> str:
        """Get last git tag"""
        try:
            result = subprocess.run(
                ["git", "describe", "--tags", "--abbrev=0"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None
    
    def _get_changed_files(self) -> List[str]:
        """Get list of changed files since last tag"""
        last_tag = self._get_last_tag()
        
        if last_tag:
            cmd = ["git", "diff", f"{last_tag}..HEAD", "--name-only"]
        else:
            cmd = ["git", "diff", "--name-only", "--cached"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return [f for f in result.stdout.strip().split('\n') if f]
        except subprocess.CalledProcessError:
            return []
    
    def detect_changes(self) -> Dict[str, bool]:
        """Detect what components changed"""
        changes = {
            "codex": False,
            "flows": False,
            "ui": False,
            "api": False,
            "docker": False,
            "k8s": False
        }
        
        changed_files = self._get_changed_files()
        
        for file_path in changed_files:
            # QDPI Core/Codex changes
            if any(path in file_path for path in ['qdpi.py', 'symbols/', 'generate_symbols.py', 'srec/']):
                changes["codex"] = True
            
            # Flow system changes
            elif any(path in file_path for path in ['qdpi_flows.py', 'flows/', 'workflows/']):
                changes["flows"] = True
            
            # UI/Frontend changes
            elif any(path in file_path for path in ['src/', 'components/', 'pages/', 'frontend/']):
                changes["ui"] = True
            
            # API changes
            elif any(path in file_path for path in ['api/', 'main.py', 'websocket', 'routes/']):
                changes["api"] = True
                
            # Infrastructure changes
            elif any(path in file_path for path in ['Dockerfile', 'docker-compose', 'requirements']):
                changes["docker"] = True
                
            elif any(path in file_path for path in ['k8s/', 'kubernetes/', '.yml', '.yaml']):
                changes["k8s"] = True
        
        return changes
    
    def calculate_bump_type(self, changes: Dict[str, bool]) -> str:
        """Calculate version bump type based on changes"""
        if changes["codex"]:
            # QDPI codex changes are major (breaking changes to symbolic system)
            return "major"
        elif changes["flows"] or changes["api"]:
            # Flow or API changes are minor (new features)
            return "minor"
        else:
            # UI, docker, k8s changes are patch (improvements)
            return "patch"
    
    def bump_version(self, bump_type: str = None) -> Dict[str, any]:
        """Bump version based on changes"""
        version = self.get_current_version()
        changes = self.detect_changes()
        
        if bump_type is None:
            bump_type = self.calculate_bump_type(changes)
        
        print(f"🔄 Detected changes: {[k for k, v in changes.items() if v]}")
        print(f"📈 Bump type: {bump_type}")
        
        # Bump component versions
        if changes["codex"]:
            version["codex_version"] = self._bump_semver(version["codex_version"], bump_type)
            print(f"  📦 Codex: {version['codex_version']}")
            
        if changes["flows"]:
            version["flows_version"] = self._bump_semver(version["flows_version"], "minor" if bump_type == "major" else bump_type)
            print(f"  ⚡ Flows: {version['flows_version']}")
            
        if changes["ui"]:
            version["ui_version"] = self._bump_semver(version["ui_version"], "minor" if bump_type == "major" else bump_type)
            print(f"  🎨 UI: {version['ui_version']}")
            
        if changes["api"]:
            version["api_version"] = self._bump_semver(version["api_version"], bump_type)
            print(f"  🔗 API: {version['api_version']}")
        
        # Bump main version
        old_version = f"{version['major']}.{version['minor']}.{version['patch']}"
        
        if bump_type == "major":
            version["major"] += 1
            version["minor"] = 0
            version["patch"] = 0
        elif bump_type == "minor":
            version["minor"] += 1
            version["patch"] = 0
        else:
            version["patch"] += 1
        
        new_version = f"{version['major']}.{version['minor']}.{version['patch']}"
        print(f"🚀 Version: {old_version} → {new_version}")
        
        # Update metadata
        version["timestamp"] = datetime.now().isoformat()
        version["commit"] = self._get_commit_hash()
        version["changes"] = changes
        version["bump_type"] = bump_type
        
        # Save version
        with open(self.version_file, 'w') as f:
            json.dump(version, f, indent=2)
        
        return version
    
    def _bump_semver(self, version: str, bump_type: str) -> str:
        """Bump semantic version string"""
        try:
            major, minor, patch = map(int, version.split('.'))
        except ValueError:
            # Fallback for invalid version
            major, minor, patch = 1, 0, 0
        
        if bump_type == "major":
            return f"{major + 1}.0.0"
        elif bump_type == "minor":
            return f"{major}.{minor + 1}.0"
        else:
            return f"{major}.{minor}.{patch + 1}"
    
    def create_git_tag(self, version: Dict[str, any]) -> bool:
        """Create git tag for version"""
        tag_name = f"v{version['major']}.{version['minor']}.{version['patch']}"
        
        try:
            # Create annotated tag
            subprocess.run([
                "git", "tag", "-a", tag_name, 
                "-m", f"QDPI v{tag_name}\n\nCodex: {version['codex_version']}\nFlows: {version['flows_version']}\nUI: {version['ui_version']}\nAPI: {version['api_version']}"
            ], check=True)
            
            print(f"🏷️  Created tag: {tag_name}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create tag: {e}")
            return False
    
    def generate_changelog(self, version: Dict[str, any]) -> str:
        """Generate changelog for version"""
        changes = version.get("changes", {})
        changelog = [
            f"# QDPI v{version['major']}.{version['minor']}.{version['patch']}",
            f"",
            f"**Released:** {version['timestamp'][:19]}",
            f"**Commit:** {version['commit']}",
            f"**Type:** {version.get('bump_type', 'patch').title()} Release",
            f"",
            f"## Component Versions",
            f"- **QDPI Codex:** {version['codex_version']}",
            f"- **Flow System:** {version['flows_version']}",
            f"- **User Interface:** {version['ui_version']}",
            f"- **API Layer:** {version['api_version']}",
            f"",
            f"## Changes in This Release",
        ]
        
        if changes.get("codex"):
            changelog.extend([
                f"",
                f"### 🔮 QDPI Codex Updates",
                f"- Symbol definitions and relationships updated",
                f"- SREC embedding generation improvements",
                f"- Core symbolic protocol enhancements"
            ])
        
        if changes.get("flows"):
            changelog.extend([
                f"",
                f"### ⚡ Flow System Updates", 
                f"- New character flow implementations",
                f"- Enhanced symbol-to-function mappings",
                f"- Improved flow execution engine"
            ])
        
        if changes.get("ui"):
            changelog.extend([
                f"",
                f"### 🎨 User Interface Updates",
                f"- Enhanced QDPI interaction components",
                f"- Improved real-time state visualization",
                f"- Better WebSocket event handling"
            ])
        
        if changes.get("api"):
            changelog.extend([
                f"",
                f"### 🔗 API Updates",
                f"- New session management endpoints",
                f"- Enhanced WebSocket event system", 
                f"- Improved error handling and validation"
            ])
        
        if changes.get("docker") or changes.get("k8s"):
            changelog.extend([
                f"",
                f"### 🚀 Infrastructure Updates",
                f"- Production deployment improvements",
                f"- Enhanced monitoring and observability",
                f"- Security and performance optimizations"
            ])
        
        changelog.extend([
            f"",
            f"## 16-System Architecture Alignment",
            f"",
            f"This release maintains alignment with the Gibsey 16-system architecture:",
            f"- **Symbolic Layer (glyph_marrow):** QDPI-256 protocol core",
            f"- **Search Intelligence (london_fox):** Semantic symbol discovery", 
            f"- **Orchestration (princhetta):** Production deployment systems",
            f"- **State Management (new_natalie_weissman):** Session persistence",
            f"- **Security (cop-e-right):** API key management and access control",
            f"",
            f"---",
            f"",
            f"*Generated by QDPI Version Manager (oren_progresso)*"
        ])
        
        return "\n".join(changelog)

def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="QDPI Version Manager")
    parser.add_argument("--bump", choices=["major", "minor", "patch"], 
                       help="Force specific bump type")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be done without making changes")
    parser.add_argument("--create-tag", action="store_true",
                       help="Create git tag after version bump")
    parser.add_argument("--changelog", action="store_true",
                       help="Generate changelog")
    
    args = parser.parse_args()
    
    manager = QDPIVersionManager()
    
    if args.dry_run:
        print("🧪 DRY RUN - No changes will be made")
        changes = manager.detect_changes()
        bump_type = args.bump or manager.calculate_bump_type(changes)
        print(f"Would bump version with type: {bump_type}")
        print(f"Changes detected: {[k for k, v in changes.items() if v]}")
        return
    
    # Bump version
    version = manager.bump_version(args.bump)
    
    # Create git tag
    if args.create_tag:
        manager.create_git_tag(version)
    
    # Generate changelog
    if args.changelog:
        changelog = manager.generate_changelog(version)
        changelog_file = f"CHANGELOG_v{version['major']}.{version['minor']}.{version['patch']}.md"
        
        with open(changelog_file, 'w') as f:
            f.write(changelog)
        
        print(f"📝 Generated changelog: {changelog_file}")
    
    print("✅ Version management complete!")

if __name__ == "__main__":
    main()
resource "google_container_cluster" "primary" {
  name     = "my-gke-cluster"
  location = var.location

  remove_default_node_pool = true
  initial_node_count       = 1
}

resource "google_container_node_pool" "primary_preemptible_nodes" {
  name       = "my-node-pool"
  location   = var.location
  cluster    = google_container_cluster.primary.name
  node_count = 1

  node_config {
    preemptible  = true
    machine_type = "e2-small"
    disk_size_gb = 20
    disk_type    = "pd-standard"
    image_type   = "COS_CONTAINERD"
  }
}

resource "google_compute_disk" "kubernetes-storage" {
  name = "kubernetes-storage-disk"
  type = "pd-standard"
  size = 20
  labels = {
    environment = "dev"
  }
}